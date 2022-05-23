import shutil
import os
import re
import tarfile
from collections import OrderedDict
from importlib import import_module
from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.apps import apps
from django.core import management
from django.shortcuts import redirect
from modules_installation.templatetags.modules_tags import get_modules
from virtualhost.templatetags.virtualhost_tags import update_module_permissions_names
from virtualhost.views import update_module_permissions
from xmppserverui.mixins import PageContextMixin
from .forms import UploadModuleFileForm
from .utils.config_generator import make_xmpp_config
from django.template.utils import get_app_template_dirs

from .utils.module_spec import get_spec, is_older_version, convert_spec

SETTINGS_TAB_MODULES = 'modules'


class ManageModulesView(PageContextMixin, TemplateView):
    page_section = 'modules'
    template_name = 'modules/modules_list.html'

    def get(self, request, *args, **kwargs):
        modules = get_modules()
        context = {
            'modules': modules,
            'active_tab': SETTINGS_TAB_MODULES
        }

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        try:
            module_to_del = request.POST.get('delete_module').split('.')[1]
            module_config = apps.get_app_config(module_to_del)
            rollback_install(new_app_name=module_config.name, folder_path=module_config.path,
                             folder=module_config.label)
            return HttpResponseRedirect(reverse('server:modules-list'))
        except Exception as err:
            return self.render_to_response(context={'delete_error': err})


class UploadModuleFileView(PageContextMixin, TemplateView):
    page_section = 'modules_upload'
    template_name = 'modules/upload_module.html'

    def get(self, request, *args, **kwargs):
        form = UploadModuleFileForm()
        context = {
            'form': form,
        }
        return self.render_to_response(context=context)

    def post(self, request, *args, **kwargs):
        form = UploadModuleFileForm(request.POST, request.FILES)
        if form.is_valid():
            error = self.handle_uploaded_file(request.FILES['file'])
            if error:
                return self.render_to_response({'form': form, 'error': error})
            else:
                return HttpResponseRedirect(reverse('server:modules-list'))
        return self.render_to_response({'form': form})

    def handle_uploaded_file(self, f):
        try:
            tar = tarfile.open(fileobj=f.file, mode='r:gz')
            module_spec = [el for el in tar.getmembers() if el.path.endswith('module.spec')]
            if not module_spec:
                tar.close()
                return 'Something went wrong during the installation of this module: {}' \
                    .format('module does not have a required file module.spec.')
            file_spec = tar.extractfile(module_spec[0]).read().decode('utf-8')
            spec = convert_spec(file_spec)
            spec_module_name = spec.get('name')
            dir_module_name = module_spec[0].name.split('/')[1]
            if spec_module_name != dir_module_name.strip():
                tar.close()
                return 'Something went wrong during the installation of this module: {}' \
                    .format('mismatch between module folder name and module name in specification.')
            module_exist = 'modules.{}'.format(spec_module_name) in settings.INSTALLED_APPS
            if module_exist:
                current_module_spec = get_spec(spec_module_name)
                cur_ver = current_module_spec.get('version')
                new_ver = spec.get('version')
                if is_older_version(cur_ver, new_ver):
                    tar.close()
                    return 'Something went wrong during the installation of this module: {}' \
                        .format('Version of loaded module is older than current or incorrect version format in spec.')
            subdir_and_files = []
            for member in tar.getmembers():
                if member.path.startswith('panel/'):
                    member.path = member.path[len('panel/'):]
                    subdir_and_files.append(member)
            tar.extractall(settings.MODULES_DIR, members=subdir_and_files)
            tar.close()
        except tarfile.ReadError:
            return 'Module files cannot be extracted from this file'

        if os.path.exists(settings.MODULES_DIR):
            for folder in os.listdir(settings.MODULES_DIR):
                folder_path = os.path.join(settings.MODULES_DIR, folder)
                if os.path.isdir(folder_path):
                    new_app_name = "modules." + folder
                    if not apps.is_installed(new_app_name):
                        try:
                            apps.app_configs = OrderedDict()
                            settings.INSTALLED_APPS += (new_app_name,)
                            apps.apps_ready = apps.models_ready = apps.loading = apps.ready = False
                            apps.clear_cache()
                            apps.populate(settings.INSTALLED_APPS)
                            if os.path.exists(os.path.join(folder_path, 'migrations', '__init__.py')):
                                management.call_command('migrate', folder, interactive=False)
                            update_module_permissions()
                            update_module_permissions_names()
                            make_xmpp_config()
                            get_app_template_dirs.cache_clear()
                        except Exception as err:
                            rollback_install(new_app_name, folder_path, folder)
                            return 'Something went wrong during the installation of this module: {}.'.format(err)
            return ''


def module_view_detail(request, module, path):
    try:
        urlconf = import_module("modules." + module + '.urls')
        patterns = getattr(urlconf, 'urlpatterns')
        path_patterns = list(filter(lambda x: re.match(str(x.pattern), path), patterns))
        if len(path_patterns):
            return path_patterns[0].callback(request)
        else:
            return redirect('server:dashboard')
    except ImportError or AttributeError:
        return redirect('server:dashboard')


def rollback_install(new_app_name, folder_path, folder):
    try:
        management.call_command('migrate', folder, 'zero', interactive=False)
    except:
        pass
    try:
        settings.INSTALLED_APPS.remove(new_app_name)
    except:
        pass
    try:
        shutil.rmtree(folder_path)
    except:
        pass
    try:
        del apps.app_configs[folder]
    except:
        pass
    try:
        del apps.all_models[folder]
    except:
        pass
    update_module_permissions()
    update_module_permissions_names()
    make_xmpp_config()

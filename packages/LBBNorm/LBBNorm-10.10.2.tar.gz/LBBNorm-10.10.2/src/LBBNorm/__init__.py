from importlib import import_module

def lazy_load(module_name, package_name):
    return lambda: import_module(module_name, package=package_name)

package_name = __package__

Macenko = lazy_load('.macenko.Macenko', package_name)
Vahadane = lazy_load('.vahadane.Vahadane', package_name)
AdaptiveColorDeconvolution = lazy_load('.adaptive_color_deconvolution.AdaptiveColorDeconvolution', package_name)
Reinhard = lazy_load('.reinhard.Reinhard', package_name)
ModifiedReinhard = lazy_load('.modified_reinhard.ModifiedReinhard', package_name)
WholeSlidePatcher = lazy_load('.slide_patcher.WholeSlidePatcher', package_name)

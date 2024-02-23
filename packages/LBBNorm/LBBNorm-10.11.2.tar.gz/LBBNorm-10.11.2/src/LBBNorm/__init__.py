from importlib import import_module

def lazy_load(module_name):
    package_name = __name__.rpartition('.')[0]  # Get the package name dynamically
    full_module_name = f'{package_name}{module_name}'
    return lambda: import_module(full_module_name)

Macenko = lazy_load('.macenko.Macenko')
Vahadane = lazy_load('.vahadane.Vahadane')
AdaptiveColorDeconvolution = lazy_load('.adaptive_color_deconvolution.AdaptiveColorDeconvolution')
Reinhard = lazy_load('.reinhard.Reinhard')
ModifiedReinhard = lazy_load('.modified_reinhard.ModifiedReinhard')
WholeSlidePatcher = lazy_load('.slide_patcher.WholeSlidePatcher')

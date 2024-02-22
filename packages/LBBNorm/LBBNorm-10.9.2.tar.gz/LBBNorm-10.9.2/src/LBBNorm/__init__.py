from importlib import import_module

def lazy_load(module_name):
    return lambda: import_module(module_name)

Macenko = lazy_load('.macenko.Macenko')
Vahadane = lazy_load('.vahadane.Vahadane')
AdaptiveColorDeconvolution = lazy_load('.adaptive_color_deconvolution.AdaptiveColorDeconvolution')
Reinhard = lazy_load('.reinhard.Reinhard')
ModifiedReinhard = lazy_load('.modified_reinhard.ModifiedReinhard')
WholeSlidePatcher = lazy_load('.slide_patcher.WholeSlidePatcher')

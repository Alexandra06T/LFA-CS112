import CFG

try:
    # d = CFG.load_sections()
    sigma = CFG.load_sigma()
    var = CFG.load_vars()
    rules = CFG.load_rules()
    print(CFG.generate_lang())
except RuntimeError as err:
    print(err)
except Exception as err:
    print(repr(err))

from src.advisory import allocation_gap
def test_gap():
    r=allocation_gap({'Equity':.6},{'Equity':.5,'Bonds':.5}); assert any(x['asset_class']=='Bonds' and abs(x['gap']-.5)<1e-9 for x in r)

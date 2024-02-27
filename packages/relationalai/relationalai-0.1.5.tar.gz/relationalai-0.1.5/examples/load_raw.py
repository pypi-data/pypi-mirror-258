#pyright: reportUnusedExpression=false
import relationalai as rai

model = rai.Model("MyCoolDatabase")
model.load_raw("rel/bar.rel")
model.load_raw("rel/foo.rel")

with model.query() as select:
    a,b = model.Vars(2)
    model.rel.foo(a, b)
    model.rel.bar(a + 5)
    z = select(a, b)

print(z.results)







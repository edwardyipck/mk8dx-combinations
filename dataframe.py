import pandas as pd
import itertools as it


def dataframe():
    drivers = pd.read_csv("assets/data/drivers.csv")
    bodies = pd.read_csv("assets/data/bodies.csv")
    tires = pd.read_csv("assets/data/tires.csv")
    gliders = pd.read_csv("assets/data/gliders.csv")
    
    namelist = [drivers.Driver.tolist(),bodies.Body.tolist(),tires.Tires.tolist(),gliders.Glider.tolist()]
    allnames = list(it.product(*namelist))
    statlist = [drivers.drop("Driver",axis=1).values.tolist(),
                bodies.drop("Body",axis=1).values.tolist(),
                tires.drop("Tires",axis=1).values.tolist(),
                gliders.drop("Glider",axis=1).values.tolist()]
    allstats = list(it.product(*statlist))
    allstats = [[sum(x) for x in zip(i[0],i[1],i[2],i[3])] for i in allstats]
    nametable = pd.DataFrame(allnames, columns = ["Driver", "Body", "Tires", "Glider"])
    stattable = pd.DataFrame(allstats, columns = ['Weight', 'Acceleration', 'On-Road traction', '(Off-Road) Traction',
                                                  'Mini-Turbo', 'Ground Speed', 'Water Speed', 'Anti-Gravity Speed',
                                                  'Air Speed', 'Ground Handling', 'Water Handling',
                                                  'Anti-Gravity Handling', 'Air Handling'])
    
    comb = nametable.join(stattable)
    comb["Total"] = comb.sum(axis=1)
    driver_list = drivers["Driver"].to_list()
    return comb, driver_list
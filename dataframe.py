import pandas as pd
import itertools as it

def dataframe():
    datatypes = {0: 'object'}
    datatypes.update({i:'int8' for i in range(1,14)})
    
    drivers = pd.read_csv("assets/data/drivers.csv",dtype=datatypes)
    bodies = pd.read_csv("assets/data/bodies.csv",dtype=datatypes)
    tires = pd.read_csv("assets/data/tires.csv",dtype=datatypes)
    gliders = pd.read_csv("assets/data/gliders.csv",dtype=datatypes)

    driver_list = drivers["Driver"].to_list()
    
    namelist = list(it.product(*[drivers.Driver.tolist(),
                                 bodies.Body.tolist(),
                                 tires.Tires.tolist(),
                                 gliders.Glider.tolist()]
                              )
                   )
    
    namelist = pd.DataFrame(namelist, columns = ["Driver", "Body", "Tires", "Glider"],dtype='category')
    
    statlist = list(it.product(*[drivers.drop("Driver",axis=1).values.tolist(),
                            bodies.drop("Body",axis=1).values.tolist(),
                            tires.drop("Tires",axis=1).values.tolist(),
                            gliders.drop("Glider",axis=1).values.tolist()]
                          )
               )
    
    statlist = [[sum(x) for x in zip(i[0],i[1],i[2],i[3])] for i in statlist]
    statlist = pd.DataFrame(statlist, columns = ['Weight', 'Acceleration', 'On-Road traction', '(Off-Road) Traction',
                                                  'Mini-Turbo', 'Ground Speed', 'Water Speed', 'Anti-Gravity Speed',
                                                  'Air Speed', 'Ground Handling', 'Water Handling',
                                                  'Anti-Gravity Handling', 'Air Handling'],dtype='int8')
    
    namelist = namelist.join(statlist)
    namelist["Total"] = namelist.sum(axis=1).astype('uint8')
    
    return namelist, driver_list

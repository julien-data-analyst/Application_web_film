# This test script performs unitary tests for the model Collection

from modele_bdd import Collection

def test_collection_characteristics(collection: Collection):
    assert collection.id == 1
    assert collection.name == "Test collection" 
    assert collection.films.count() == 0 # chelou - film is not yet created 
    # not chelou, the relations determine why 1-m, m-1
    
    
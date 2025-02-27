# This test script performs unitary tests for the model Collection

from modele_bdd import Collection

def test_collection_characteristics(collection):
    assert collection.id == 1
    assert collection.name == "Test collection" 
    assert collection.films.count() == 0 # chelou - film is not yet created 
    
    
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import uuid

app = FastAPI()

corpora = {
    "seinfeld": {
        "person": ["jerry","george","elaine","kramer","newman","susan","helen","morty","frank","estelle","peterman","manya"],
        "place": ["monks-cafe","diner","apartment","yankees-stadium","central-park","subway","dentists","optometrist","petermans","movie-theater","del-boca-vista"],
        "thing": ["festivus-feats","puffy-shirt","muffin-tops","pony","pez-dispenser","big-salad","library-book","marble-rye","coffee","standup","mail","standup"]
    },
    "lotr": {
        "person": ["frodo","gandalf","aragorn","legolas","gimli","samwise","boromir","merry","pippin","sauron","saruman","galadriel","elrond","gollum"],
        "place": ["shire","rivendell","moria","lothlorien","rohan","gondor","isengard","mordor","prancing-pony","mines-of-moria","mount-doom","minas-tirith","helms-deep","mirkwood"],
        "thing": ["the-one-ring","sting","narsil","palantir","mithril","anduril","horn-of-helm-hammerhand","evenstar","elven-cloak","lembas-bread","arkenstone","silmarils"]
    },
    "marvel": {
        "person": ["iron-man","captain-america","thor","hulk","black-widow","hawkeye","spider-man","black-panther","doctor-strange","scarlet-witch","vision","ant-man","wasp","falcon","winter-soldier"],
        "place": ["new-york","asgard","wakanda","san-francisco","knowhere","xandar","titan","quantum-realm","sokovia","egypt","norway","atlantis","sanctum-sanctorum","randys-donuts","madripoor"],
        "thing": ["infinity-gauntlet","mjolnir","shield","arc-reactor","vibranium","tesseract","eye-of-agamotto","web-shooters","nanotech","cloak-of-levitation","pym-particles","adamantium"]
    }
}

class Payload(BaseModel):
    c: str
    p: str | None = None

@app.post("/random")
def generate_random_bucket_name(payload: Payload):
    if payload.c not in ['seinfeld', 'lotr', 'marvel']:
        raise HTTPException(status_code=400, detail="Invalid value for parameter 'c'. Valid values are 'seinfeld', 'lotr', or 'marvel'.")

    corpus = corpora[payload.c]
    person = random.choice(corpus["person"])
    place = random.choice(corpus["place"])
    thing = random.choice(corpus["thing"])
    unique_id = str(uuid.uuid4()).split('-')[-1]

    if payload.p:
        bucket_name = f"{payload.p}-{place}-{thing}-{unique_id}"
    else:
        bucket_name = f"{person}-{place}-{thing}-{unique_id}"
    
    return {"bucket_name": bucket_name}
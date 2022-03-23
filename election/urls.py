from django.urls import path

from .views import *

app_name="election"

urlpatterns = [
    path(r"", liste_candidats, name="liste_candidats"),
    path("candidat/liste", liste_candidats, name="liste_candidats"),
    path("candidat/detail/<int:id_candidat>", detail_candidat, name="detail_candidat"),
    path("candidat/ajout", ajout_candidat, name="ajout_candidat"),
    path("bureau/liste", liste_bureaux, name="liste_bureaux"),
    path("bureau/ajout", ajout_bureau, name="ajout_bureau"),
    path("electeur/ajout", ajout_electeur, name="ajout_electeur"),
    path("electeur/liste", liste_electeurs, name="liste_electeurs"),
    path("conseil/liste", ConseilList.as_view(), name="liste_conseils"),
    path("conseil/ajout", ConseilCreate.as_view(), name="ajout_conseil"),
    path("vote/", VoteView.as_view(), name="vote"),
    path("resultats/", ResultatsView.as_view(), name="resultats"),
]

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *

# Create your views here.
def liste_candidats(request):
    #Vue renvoyant à l'utilisateur la liste des candidats de l'élection
    candidats = Candidat.objects.all()
    contexte = {
        'liste' : candidats
    }
    return render(request, 'election/candidats.html', contexte)


def detail_candidat(request, id_candidat):
    #Vue renvoyant le détail d'un candidat
    candidat = get_object_or_404(Candidat, pk=id_candidat)
    return render(request, 'election/candidat.html', {'candidat' : candidat})


def ajout_candidat(request):
    #Vue permettant l'ajout d'un nouveau candidat
    if request.method == 'POST':
        form = CandidatForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/candidat/liste')
    else:
        form = CandidatForm()
        return render(request, 'election/ajout_candidat.html', {'form' : form})


def ajout_bureau(request):
    # Vue permettant l'ajout d'un nouveau bureau de vote
    if request.method=="POST":
        form = BureauForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('election:liste_bureaux')
    form = BureauForm()
    return render(request, 'election/ajout_bureau.html', {'form' : form})

def liste_bureaux(request):
    #Liste des bureaux
    bureaux = Bureau.objects.all()
    return render(request, 'election/bureaux.html', {'bureaux' : bureaux})


def ajout_electeur(request):
    #Vue pour ajouter un nouvel électeur
    if request.method=="POST":
        form = UserForm(request.POST)
        formset = ElecteurFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            formset.instance = user
            if formset.is_valid():
                formset.save()
                return redirect('election:liste_electeurs')
        else:
            return render(request, 'election/ajout_electeur.html', {'form' : form, 'formset' : formset})
    form = UserForm()
    formset = ElecteurFormSet()
    contexte = {
        'form' : form,
        'formset' : formset
    }
    return render(request, 'election/ajout_electeur.html', contexte)


@login_required
def liste_electeurs(request):
    # Liste des électeurs
    electeurs = Electeur.objects.all()
    return render(request, 'election/electeurs.html', {'electeurs' : electeurs})


class ConseilCreate(CreateView):
    model = User
    fields = ['first_name', 'last_name', 'username', 'password']
    template_name = 'election/ajout_conseil.html'
    success_url = reverse_lazy('election:liste_conseils')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['password'])
        self.object.save()
        Conseil.objects.create(user=self.object)
        return redirect(self.success_url)



class ConseilList(ListView):
    model = Conseil
    template_name = 'election/conseils.html'


class VoteView(LoginRequiredMixin, View):
    """
    View permettant à un utilisateur d'effectuer un vote
    """
    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.electeur_set.first().a_vote:
            return redirect('election:resultats')
        form = VoteForm()
        return render(request, 'election/vote.html', {'form' : form})

    def post(self, request, *args, **kwargs):
        form = VoteForm(request.POST)
        if form.is_valid():
            candidat = form.cleaned_data['candidats']
            user = request.user
            electeur = user.electeur_set.first()
            electeur.vote(candidat)
            candidat.ajout_vote() #On incrémente le nb_voix
            return redirect('election:resultats')


class ResultatsView(ListView):
    model = Candidat
    template_name = 'election/resultats.html'



from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView

from wishes.forms import WishForm, MemberForm, FamilyForm
from wishes.models import Wish, Member, Present, Family
from wishes.templatetags.tags import get_family_id, get_user_id, get_family
from django.utils.translation import gettext_lazy as _


def index(request):
    if request.user.is_authenticated:
        user = request.user
        control_members = Member.objects.filter(user=user)
        return render(request, 'home.html',
                      {'members': control_members})
    return render(request, 'base.html')


class AddWishView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'
    form_class = WishForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy("my-wish-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['member'].queryset = Member.objects.filter(user=self.request.user)
        return form


class MyWishListView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        members = Member.objects.filter(user_id=get_user_id(request))
        return render(request, 'mywishlist.html', {'members': members})


class PresentListView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        id = get_user_id(request)
        presents = Present.objects.filter(user_id=id).order_by('is_bought')
        return render(request, 'presentlist.html', {'objects': presents})



class AddMemberView(CreateView):
    form_class = MemberForm
    template_name = "form.html"

    def get_success_url(self):
        return reverse_lazy("main")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        family = get_family(self.request)
        if Member.objects.filter(name=obj.name, family=family).exists():
            form.add_error('name', "Taki użytkownik istnieje")
            return self.form_invalid(form)
        else:
            obj.family = get_family(self.request)
            obj.main_member = False
            obj.save()
            self.object = obj
            return HttpResponseRedirect(self.get_success_url())


class AddMainMemberView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request, id):
        form = MemberForm()
        header = "Teraz stwórz swojego członka rodziny - po prostu wpisz swoje imię i datę urodzenia :)"
        return render(request, 'form.html', {'form': form, 'id': id, 'header':header})

    def post(self, request, id):
        form = MemberForm(request.POST)
        obj = form.save(commit=False)
        obj.user = request.user
        family = Family.objects.get(id=id)
        if Member.objects.filter(name=obj.name, family=family).exists():
            error = "Taki użytkownik istnieje"
            return render(request, 'form.html', {'form': form, 'id': id, 'header':error})
        obj.main_member = True
        obj.family=family
        obj.save()
        return redirect('/')


class AddFamilyView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        form = FamilyForm()
        header = "Jesteś pierwszym członkiem rodziny! Stwórz dla niej jakąś nazwę, może to być na przykład nazwisko"
        return render(request, 'form.html', {'form': form, 'header':header})

    def post(self, request):
        form = FamilyForm(request.POST)
        if form.is_valid():
            obj = form.save()
            id = obj.id
            return redirect(f'/add-main-member/{id}')
        return render(request, 'registration/signup.html', {'form': form})


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy("add-family")

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class SignUpFamilyView(View):

    def get(self, request, id):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form, 'id': id})

    def post(self, request, id):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return redirect(f'/add-main-member/{id}')
        return render(request, 'registration/signup.html', {'form': form, 'id': id})



class BookWish(View):

    def post(self, request):
        wish_id = request.POST.get("wish_id")
        user = request.user
        Present.objects.create(wish_id=wish_id, user_id=user.id)
        return redirect(f"/wish-list")


class DeleteWish(View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        wish_id = request.GET.get("wish_id")
        question = "Czy na pewno nie chcesz dostać"
        wish = Wish.objects.get(id=wish_id)
        name = wish.name
        return render(request, 'delete.html', {"question":question, "object":wish, "name":name})

    def post(self, request):
        wish_id = request.POST.get("id")
        Wish.objects.get(id=wish_id).delete()
        return redirect("/my-wish-list")

# DO ZMIANY
class EditWish(UpdateView):
    model = Wish
    fields = ['name', 'description', 'link', 'member']
    template_name = 'form.html'
    success_url = '/my-wish-list'
    labels = {
        'name': _('Co chcesz dostać?'),
        'description': _('Opowiedz coś więcej ;)'),
        'link': _('A może masz upatrzony już konkretny model? Wrzuć nam linka ;)'),
        'member': _('Wybierz członka rodziny, którego to życzenie :) (jeśli go tu nie ma, musisz go najpierw dodać!')
    }

    def get_object(self, queryset=None):
        obj = Wish.objects.get(id=self.kwargs['id'])
        return obj

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['member'].queryset = Member.objects.filter(user=self.request.user)
        return form

class DeletePresent(View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        present_id = request.GET.get("present_id")
        question = "Czy na pewno nie chcesz zarezerwować prezentu"
        present = Present.objects.get(id=present_id)
        name = present.wish.name
        return render(request, 'delete.html', {"question": question, "object": present, "name":name})

    def post(self, request):
        present_id = request.POST.get("id")
        Present.objects.get(id=present_id).delete()
        return redirect("present-list")


class BuyPresent(View):
    def post(self, request):
        present_id = request.POST.get("present_id")
        present = Present.objects.get(id=present_id)
        present.is_bought = not present.is_bought
        present.save()
        return redirect(f"/present-list")


class WishView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    redirect_field_name = 'next'

    def get(self, request):
        family_id = get_family_id(request)
        user_id=get_user_id(request)
        user_member_id = Member.objects.filter(user_id=user_id).get(main_member=True).id
        members = Member.objects.filter(family=family_id).exclude(id=user_member_id)
        presents = Present.objects.filter(user_id=user_id)
        wishes = Wish.objects.filter(present__in=presents)
        members_done = members.filter(wishes__in=wishes).distinct()
        members = members.exclude(wishes__in=wishes)
        return render(request, 'wishes.html', {'members': members, 'members_done':members_done})

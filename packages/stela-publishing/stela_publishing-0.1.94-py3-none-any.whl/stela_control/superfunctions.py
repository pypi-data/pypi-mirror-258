import re, datetime, ast, time, openai, requests, jwt, json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.contrib.auth import login, logout, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.utils.encoding import force_bytes, force_str
from accounts.token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from datetime import timedelta
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from stela_control.context_processors import SiteData
from django.conf import settings
from pytz import country_timezones
from django.forms import formset_factory, inlineformset_factory
from django.http.response import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from accounts.models import UserBase
from django.shortcuts import render, redirect
from .models import (
    Content, Wallet, DataEmail, 
    DynamicBullets, Newsletter, SendMoney, BillingRecipt,
    ItemProducts, ItemServices, ItemDiscount,  
    InvoiceControl, BudgetControl, StelaSelection, 
    StelaItems, Templates, Order, StelaPayments, PathControl, 
    ControlFacturacion, FacturaItems, TemplateSections, StelaColors,
    ModuleItems, ProStelaData, OrderItems, Inventory, Elements, 
    Variant, Sizes, Gallery, Bulletpoints, Sizes, VariantsImage, Customer, 
    Budget, Category, SitePolicy, LegalProvision, SupportResponse, 
    Support, ChatSupport, SiteControl, ItemCloud, FacebookPage, InstagramAccount, FacebookPostPage, FacebookPageComments, FacebookPageCommentsReply, FacebookPageConversations,
    FacebookPageEvent,  FacebookPageLikes, FacebookPageMessages, FacebookPageShares, FacebookPostMedia, IGMediaContent, FacebookPageImpressions,
    IGPost, IGUserTag, FAQ, SetFaq, Contact,Comments, PaypalClient, Notifications,
    IGPostMetric, IGCarouselMetric, IGReelMetric, IGStoriesMetric, Company, SocialLinks, ProStelaExpert, ProStelaUsage, Reviews,
    Booking, BookingServices, City, Team, JobApplication, ProfileGallery
    
)
from .forms import (
    FAQForm, NewsletterForm, PolicyForm, BillingForm, BillingDiscountForm, 
    ElementsForm,TemplateForm, ProductForm, StylesForm, 
    TempSecForm, ColorsForm, VariantForm, SizeForm, GalleryForm, BulletForm, 
    WorksForm, VariantImageForm, BillingChargeFormDynamic, BillingChargeFormPOS, 
    BillingFormSuscription, AppstelaForm, LegalProvitionForm, StelaAboutForm, 
    PathForm, MediaForm, FooterContentForm, categForm, StaffForm,
    BulletSimpleForm, CommentsFormBlog, ReadOnlySupportForm, WalletForm,
    FbPostForm, FacebookEventsForm, IGPostForm, IGMediaForm, RequiredFormSet, CompanyForm, SocialMediaForm,
    SendGridForm,BlogFormImage,BlogFormVideo,ContentForm, RedirectContentForm, StickerContentForm, ContentDynamicForm,
    SimpleContentForm, SetFaqForm, ImageContentForm, TitleContentForm, AboutContentForm, ReviewsForm,
    ConsultingForm, BookingConsultingForm, RegistrationForm, UserEditForm, UserPortalForm, UserLoginForm, PwdResetForm, 
    PwdResetConfirmForm, ValuesForm, LoginForm, JobApplicationForm, CatalogForm, StaffGalleryForm, WorksReviewsForm, 
    WorksReviewsCommentsForm, CommentsWorks, EditCompanyForm, SupportForm, MasterContactForm, MasterReviewsForm,
    MasterCommentsFormBlog, MasterSupportForm, ChatSupportForm
)
form_mapping = {
    #Content
    'TitleContentForm': TitleContentForm,
    'SimpleContentForm': SimpleContentForm,
    'ContentForm': ContentForm,
    'ContentDynamicForm': ContentDynamicForm,
    'RedirectContentForm': RedirectContentForm,
    'StickerContentForm': StickerContentForm,
    'GalleryForm': GalleryForm,
    'BulletSimpleForm': BulletSimpleForm,
    'ImageContentForm': ImageContentForm,
    'LegalProvitionForm': LegalProvitionForm,
    'FAQForm': FAQForm,
    'SetFaqForm': SetFaqForm,
    'BlogFormImage': BlogFormImage,
    'BlogFormVideo': BlogFormVideo,
    'ValuesForm': ValuesForm,
    'ProductForm': ProductForm,
    'WorksForm': WorksForm,
    'VariantForm': VariantForm,
    'ElementsForm': ElementsForm,
    'CatalogForm': CatalogForm,
    'WorksReviewsForm': WorksReviewsForm,
    'WorksReviewsCommentsForm': WorksReviewsCommentsForm,
    'SupportForm': SupportForm,
    'MasterContactForm': MasterContactForm,
    'MasterReviewsForm': MasterReviewsForm,
    'MasterCommentsFormBlog': MasterCommentsFormBlog,
    'CompanyForm':CompanyForm,
    'EditCompanyForm': EditCompanyForm,
    'SocialMediaForm': SocialMediaForm,
    'UserEditForm': UserEditForm,
    'EditCompanyForm': EditCompanyForm,
    #Inventory
    'Inventory': Inventory,
    'Elements': Elements,
    'Variant': Variant,
    'Content': Content,
    'CommentsWorks': CommentsWorks,
    'Support': Support,
    'ChatSupport': ChatSupport,
    'Company': Company,
    'SocialLinks': SocialLinks
}

SECRET_KEY = settings.STELA_SECRET

def get_form_class_by_name(form_name):
    return form_mapping[form_name]

def accountsData(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        userpk = request.POST.get('userid')
        form_name = request.POST.get('form_name')
        form_id = request.POST.get('form-id')
        pk = request.POST.get('pk')
        domain = request.POST.get('domain')
        print(action, userpk, form_name, form_id, pk, domain)
        
        if action == 'cityCheck':
            country_id = request.POST.get('country_id')
            cities = City.objects.filter(country_id=country_id)
        
            return render(request, 'stela_control/load-data/city_data.html', {'cities': cities})

        if action == "checkEmail":
            pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            email = request.POST.get("user_input")
            if UserBase.objects.filter(email=email).exists():
                response = JsonResponse({'error': _('email not available')})
            elif not pattern.match(email):
                response = JsonResponse({'error': _('Invalid email')})
            else:
                response = JsonResponse({'success': _('email available')})
            return response

        if action == "checkUsername":
            username = request.POST.get("user_input")
            if UserBase.objects.filter(username=username).exists():
                response = JsonResponse({'error': _('username not available')})
                
            elif not re.match(r'^[a-z0-9_]+$', username):
                response = JsonResponse({'error': _('invalid username only lower case, numbers and (_) accepted')})
            
            else:
                response = JsonResponse({'success': _('username available')})
            
            return response
            
        if action == "checkPassword":
            password = request.POST.get("password")
            
            if len(password) < 8:
                response = JsonResponse({'error': _('Password must be at least 8 characters long')})
            
            elif not re.match(r'^[a-zA-Z0-9*.$_]+$', password):
                response = JsonResponse({'error': _('Password must contain only alphanumeric and special characters (a-zA-Z0-9*$_.)')})
            
            elif password.isalpha():
                response = JsonResponse({'error': _('Password must contain at least one number')})
                
            else:
                response = JsonResponse({'success': _('Password is valid')})

            return response

        if action == "matchPassword":
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")

            if password1 != password2:
                response = JsonResponse({'error': _('Password dismatch.')})
            else:
                response = JsonResponse({'success': _('Password match')})
            return response

        if action == "checkEditUser":
            obj=UserBase.objects.get(pk=userpk)
            form=UserEditForm(instance=obj)
            get_formset = inlineformset_factory(
                UserBase, SocialLinks, 
                form=SocialMediaForm,
                extra=0, can_delete=True,
                )
            formset=get_formset(instance=obj, prefix='formset')
            obj_data = render_to_string('stela_control/load-data/profile/dynamic-form.html', {
                            'form': form,  
                            'formset': formset,
                            'form_name': form_name,
                            'pk': userpk
                })
            
            response = JsonResponse({'content': obj_data})
            return response

        if action == "checkPortalUser":
            obj=UserBase.objects.get(pk=userpk)
            form=UserPortalForm(instance=obj)
            obj_data = render_to_string('stela_control/load-data/profile/single-form.html', {
                            'form': form,  
                            'form_name': form_name,
                            'pk': userpk
                })
            
            response = JsonResponse({'content': obj_data})
            return response
        
        if action == "password_reset":
            form=PwdResetForm() 
            obj_data = render_to_string('stela_control/load-data/auth/pw_reset/password_reset_form.html', {
                    'form': form, 
                })
            
            response = JsonResponse({'content': obj_data})
            return response
        
        if form_id == "editUserForm":
            obj=UserBase.objects.get(pk=pk)
            form=UserEditForm(request.POST, request.FILES, instance=obj) 
            get_formset = inlineformset_factory(
                    UserBase, SocialLinks, 
                    form=SocialMediaForm,
                    extra=0, 
                    can_delete=True,
                    validate_min=True, 
                    min_num=0
                )
            formset=get_formset(request.POST, prefix='formset', instance=obj)
            if all([form.is_valid(), 
                    formset.is_valid(),
                    ]):
                parent_user = form.save(commit=False)
                parent_user.save()
                
                instances = formset.save(commit=False)
                for obj in formset.deleted_objects:
                    obj.delete()
                                
                for form in instances:
                    form.parent_user = parent_user
                    form.save()

                return JsonResponse({'success':_('Your profile has been updated')})
            else:
                print(form.errors)
                print(formset.errors)
                obj_data = render_to_string('stela_control/load-data/profile/dynamic-form.html', { 
                    'form': form,
                    'formset': formset,
                    'form_name': form_id,
                    'pk': pk
                }
            )
            return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if form_id == "PortalUserForm":
            obj=UserBase.objects.get(pk=pk)
            form=UserPortalForm(request.POST, request.FILES, instance=obj) 
            if form.is_valid():
                form.save()                   
                return JsonResponse({'success':_('Portal User has been updated')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/profile/single-form.html', { 
                    'form': form,
                    'form_name': form_id,
                    'pk': pk
                }
            )
            return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

        if form_id == "login":
            form = LoginForm(request.POST or None)
            redirectUrl = f'https://portal.{domain}/console'
            if form.is_valid():
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request,user)
                    return JsonResponse({'success': redirectUrl})
                else:
                    return JsonResponse({'alert': _('The data entered is not in our records')})

            else: 
                print(form.errors)

                return JsonResponse({'failed': _('Incorrect username or password')})
            
        if form_id == "sign-up":
            form = RegistrationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.set_password(form.cleaned_data['password1'])
                user.is_active = False
                user.save()
                if UserBase.objects.filter(newsletter=True):
                    data = DataEmail.objects.filter(email=user.email)
                    if data.exists():
                        pass
                    else:
                        DataEmail.objects.create(
                            email = user.email,
                            date = timezone.now()
                    ) 
                current_site = get_current_site(request)
                subject = _('Activate your account')
                html_content = render_to_string('email_template/registration/registration_confirm.html', {
                            'user': user,           
                            'domain': 'stela.localhost:8000',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                            })
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.DEFAULT_EMAIL,
                    [user.email]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()

                subject = _('New User On Your Site')
                html_content = render_to_string('email_template/registration/alert.html', {
                            'user': user,           
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                            })
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    subject,
                    text_content,
                    settings.STELA_EMAIL,
                    [settings.DEFAULT_EMAIL]
                )
                email.attach_alternative(html_content, "text/html")
                email.send()
                html_success = render_to_string('stela_control/load-data/auth/signup/success_register.html', { 
                    'email': user.email,
                })
                return JsonResponse({'success': _('Ok'), 'formset_html': html_success})
            else:
                html_alert = render_to_string('stela_control/load-data/auth/signup/register_errors_v1.html', { 
                    'form': form
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': html_alert})

        if form_id == "send_reset":
            form = PwdResetForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data['email']
                user_email = UserBase.objects.filter(email=data)
                if user_email.exists():
                    for user in user_email:
                        current_site = get_current_site(request)
                        subject = _('Password Reset')
                        html_content = render_to_string('email_template/password_reset/password_reset.html', {
                            'user': user,       
                            'email': user.email,    
                            'domain': 'stela.localhost:8000',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
                        text_content = strip_tags(html_content)

                        email = EmailMultiAlternatives(
                            subject,
                            text_content,
                            settings.DEFAULT_EMAIL,
                            [user.email]
                        )
                        email.attach_alternative(html_content, "text/html")
                        email.send()
                        return JsonResponse({'granted': _('The password reset link has been sent to your email')})
                else:
                    return JsonResponse({'alert_pw': _('The email entered is not registered')})
            else:
                return JsonResponse({'alert_pw': _('Enter a valid email address.')})

        if form_id == "reset_password":
            uid = request.POST.get('id')
            user = UserBase.objects.get(pk=uid)
            form = PwdResetConfirmForm(user, request.POST)
            if form.is_valid():
                form.save()
                return JsonResponse({'granted': _('The password has been saved successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/auth/pw_reset/form_errors.html', { 
                    'form': form
                })
                return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            
def new_password_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except Exception as e:
        user = None
        print(e)

    if user is not None and account_activation_token.check_token(user, token):
        print('validated')
        form = PwdResetConfirmForm(user)
        return render(request, 'home/auth/password_reset/index.html', {
            'form': form,
            'uid': uid
            })
    else:
        print('expired')
        return render(request, 'home/auth/password_reset/index.html', {
            'expired': 'ok',
            })

def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except:
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        external_url = 'http://portal.localhost:8000/console'
        return HttpResponseRedirect(external_url)
    else:
        return render(request, 'home/auth/registration/activation_invalid.html') 
            
def contentData(request):
    if request.method == 'POST':
        lang=request.LANGUAGE_CODE
        author=request.user
        form_id = request.POST.get('form-id')
        section = request.POST.get('section')
        ckeditor = request.POST.get('ckeditor')
        form_name = request.POST.get('check')
        remove = request.POST.get('remove')
        is_cke = request.POST.get('is_cke')
        action = request.POST.get('action')
        pk = request.POST.get('pk')
        content = None
        instance = None
        print(form_id, form_name, is_cke, action, section, ckeditor, remove, pk)      
        
        if form_name:
            form_class = get_form_class_by_name(form_name)
            content=Content.objects.filter(author=author, section=action, lang=lang)
            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=form_class,
                    extra=0, can_delete=True,
                )
                formset = get_formset(instance=author, prefix='formset', queryset=Content.objects.filter(section=action))
                obj_data = render_to_string(f'stela_control/load-data/maincontent/update_forms/{form_name}.html', { 
                    'formset': formset,
                    'form_name': form_name,
                    'section': action   
                })
                if is_cke:
                    response = JsonResponse({'content': obj_data, 'cke': is_cke})
                else:
                    response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                    form=form_class,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string(f'stela_control/load-data/maincontent/forms/{form_name}.html', { 
                    'formset': get_formset(prefix='formset'),
                    'form_name': form_name,
                    'section': action
                })
                if is_cke:
                    response = JsonResponse({'content': obj_data, 'cke': is_cke})
                else:
                    response = JsonResponse({'content': obj_data})
            return response

        if form_id:
            form_name = form_id
            form_class = get_form_class_by_name(form_name)
            if pk:
                instance=Content.objects.get(pk=pk)
            else:
                content=Content.objects.filter(author=author, section=section, lang=lang)

            if content:
                get_formset = inlineformset_factory(
                    UserBase, Content, 
                    form=form_class,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset', instance=author)
                if formset.is_valid():

                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = section
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    print(form_name)
                    obj_data = render_to_string(f'stela_control/load-data/maincontent/error_forms/{form_name}.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                        'form_name': form_name,
                        'section': section
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _(f'Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            
            elif instance:
                form = form_class(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string(f'stela_control/load-data/maincontent/error_forms/{form_name}.html', { 
                        'form': form,
                        'errors': formset.errors,
                        'form_name': form_id,
                        'section': section
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _(f'Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
                    
            else:
                get_formset = formset_factory(
                    form=form_class,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        data = form.save(commit=False)
                        data.author = author
                        data.section = section
                        data.lang = lang
                        data.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(formset.errors)
                    obj_data = render_to_string(f'stela_control/load-data/maincontent/error_forms/{form_name}.html', { 
                        'formset': formset,
                        'errors': formset.errors,
                        'form_name': form_name,
                        'section': section
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if remove:
            pk=request.POST.get('id')
            content=Content.objects.get(pk=pk)
            content.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
               
def docsData(request): 
    if request.method == 'POST':
        lang=request.LANGUAGE_CODE
        author=request.user
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        is_cke = request.POST.get('is_cke')
        ckeditor = request.POST.get('ckeditor')
        print(form_id, action, is_cke, ckeditor)
        
        if action == "checkDocs":
            pk=request.POST.get('pk')
            if pk:
                obj=SitePolicy.objects.get(pk=pk)
                form=PolicyForm(instance=obj)
                get_formset = inlineformset_factory(
                SitePolicy, LegalProvision, 
                form=LegalProvitionForm,
                extra=0, can_delete=True,
                )
                formset=get_formset(instance=obj, prefix='terms')

                obj_data = render_to_string('stela_control/load-data/site_docs/update_forms/terms.html', {
                                'form': form, 
                                'formset': formset,   
                                'pk': pk  
                    })

                if is_cke:
                    response = JsonResponse({'content': obj_data, 'cke': is_cke})
                else:
                    response = JsonResponse({'content': obj_data})
            else:
                form=PolicyForm()
                get_formset = inlineformset_factory(
                    SitePolicy, LegalProvision, 
                    form=LegalProvitionForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(prefix='terms')

                obj_data = render_to_string('stela_control/load-data/site_docs/forms/terms.html', {
                                'form': form, 
                                'formset': formset,   
                    })
                if is_cke:
                    response = JsonResponse({'content': obj_data, 'cke': is_cke})
                else:
                    response = JsonResponse({'content': obj_data})
            return response

        if action == "checkFAQ": 
            pk=request.POST.get('pk')
            if pk:   
                print(pk)
                content=FAQ.objects.get(pk=pk)
                form=FAQForm(instance=content)
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(instance=content, prefix='formset')
                obj_data = render_to_string('stela_control/load-data/site_docs/update_forms/faq_form.html', { 
                    'form': form,
                    'formset':formset,   
                    'pk': pk
                })
                if is_cke:
                    response = JsonResponse({'content': obj_data, 'cke': is_cke})
                else:
                    response = JsonResponse({'content': obj_data})
            else:
                form=FAQForm()
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/site_docs/forms/faq_form.html', { 
                    'form': form,
                    'formset': get_formset(prefix='formset')
                })
                if is_cke:
                    response = JsonResponse({'content': obj_data, 'cke': is_cke})
                else:
                    response = JsonResponse({'content': obj_data})
            return response
        
        if action == "removeDoc":
            doc_id=request.POST.get('id')
            doc=SitePolicy.objects.get(pk=doc_id)
            doc.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})

        if action == "removeFAQ":
            content_id=request.POST.get('id')
            content=FAQ.objects.get(pk=content_id)
            content.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})

        if form_id == "doc-form":
            update_form = request.POST.get('form-update')
            if update_form:
                form=PolicyForm(request.POST, instance=update_form)
                get_formset = inlineformset_factory(
                    SitePolicy, LegalProvision, 
                    form=LegalProvitionForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, prefix='terms', instance=update_form)
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    policy = form.save(commit=False)
                    policy.owner = author
                    policy.lang = lang
                    policy.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.policy = policy
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/site_docs/error_forms/terms.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                form=PolicyForm(request.POST)
                get_formset = inlineformset_factory(
                    SitePolicy, LegalProvision, 
                    form=LegalProvitionForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='terms')
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    policy = form.save(commit=False)
                    policy.owner = author
                    policy.lang = lang
                    policy.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.policy = policy
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/site_docs/error_empty_forms/terms.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        if form_id == "faq-form":
            pk = request.POST.get('form-update')
            if pk:
                content=FAQ.objects.get(pk=pk)
                form=FAQForm(request.POST, instance=content)
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0, can_delete=True,
                )
                formset=get_formset(request.POST, prefix='formset', instance=content)
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.author = author
                    parent.lang = lang
                    parent.save()
                
                    instances = formset.save(commit=False)
                                
                    for obj in formset.deleted_objects:
                            obj.delete()
                                
                    for instance in instances:
                        instance.faq = parent
                        instance.save()
                        
                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/site_docs/error_forms/faq_form.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                form=FAQForm(request.POST)
                get_formset = inlineformset_factory(
                    FAQ, SetFaq, 
                    form=SetFaqForm,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset=get_formset(request.POST, prefix='formset')
                print(form.is_valid(),
                        formset.is_valid())
                if all([form.is_valid(),
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.author = author
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.faq = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    print(form.errors)
                    print(formset.errors)
                    obj_data = render_to_string('stela_control/load-data/site_docs/error_empty_forms/faq_form.html', { 
                        'form': form,
                        'formset': formset,
                        'errors': formset.errors,
                    })
                    if ckeditor:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor})
                    else:
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

def stelaStoryData(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            action = data.get('action')
            form_name = data.get('form_name')
        except:
            action = None
            form_name = None

        form_id = request.POST.get('form-id')
        pk = request.POST.get('pk')
        lang=request.LANGUAGE_CODE
        author=request.user
        print(form_id, action, form_name)

        if action == "checkBlog":      
            form_class = get_form_class_by_name(form_name)   
            form = form_class
            if form_name == "BlogFormVideo":
                obj_data = render_to_string('stela_control/load-data/maincontent/forms/blog_form_video.html', { 
                        'form': form,
                        'form_name': form_name
                    })
            else:
                obj_data = render_to_string('stela_control/load-data/maincontent/forms/blog_form.html', { 
                        'form': form,
                        'form_name': form_name
                    })
            return JsonResponse({'empty': obj_data})
        
        if action == "postData":   
            postpk=data.get('obj')    
            country_id = str(lang).split('-')
            get_timezone = country_timezones(country_id[1])[0]
            post = Content.objects.get(pk=postpk)
            obj_data = render_to_string('stela_control/load-data/stela_story/feed-item.html', { 
                    'post': post,
                    'usertz': get_timezone,
                })
            return JsonResponse({'content': obj_data})
        
        if action == "updateFeed":   
            pk = data.get('feed_id')    
            post = Content.objects.get(pk=pk)
            form_class = get_form_class_by_name(form_name)   
            form = form_class(instance=post)
            if post.is_schedule:
                obj_data = render_to_string(f'stela_control/load-data/maincontent/update_forms/{form_name}.html', { 
                        'form': form,
                        'form_name': form_name,
                        'pk': pk
                    })
                response = JsonResponse({
                        'content': obj_data,
                        'getDate': post.schedule,
                        'pk': pk
                    })
            else:
                obj_data = render_to_string(f'stela_control/load-data/maincontent/update_forms/{form_name}.html', { 
                        'form': form,
                        'pk': pk,
                        'form_name': form_name,
                    })
                response = JsonResponse({'content': obj_data})
                
            return response
        
        if action == "removeObj":
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = Content.objects.get(pk=id)
                obj.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
        if action == "loadPages":
            lang=request.LANGUAGE_CODE
            country_id = str(lang).split('-')
            get_timezone = country_timezones(country_id[1])[0] 
            starts = int(request.POST.get('start'))
            ends = int(request.POST.get('ends'))
            print(starts)
            print(ends)
            new_posts = Content.objects.filter(author=author, lang=lang).order_by('-id')[starts:ends]
            new_pages = render_to_string('stela_control/load-data/blog-feed.html', {
                    'feed': new_posts,
                    'usertz': get_timezone,
                    })
            return JsonResponse({'response': new_pages})
        
        if form_id == "BlogFormVideo": 
            if pk:
                post=Content.objects.get(pk=pk)
                form = BlogFormVideo(request.POST, request.FILES, instance=post)
                website = request.POST.get('website')
                schedule = request.POST.get('schedule')
                if form.is_valid():
                    data = form.save(commit=False)
                    data.author = author
                    data.section = "Blog Post"
                    data.site = website
                    data.lang = lang
                    data.save()

                    if schedule:
                        Content.objects.filter(pk=data.id).update(schedule=schedule, is_schedule=True)

                    return JsonResponse({'success':_('Your post was upload successfully')})
                else:
                    print(form.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/BlogFormVideo.html', { 
                        'form': form,
                        'pk': pk,
                        'errors': form.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
            else:
                form = BlogFormVideo(request.POST, request.FILES)
                website = request.POST.get('website')
                schedule = request.POST.get('schedule')
                if form.is_valid():
                    data = form.save(commit=False)
                    data.author = author
                    data.section = "Blog Post"
                    data.site = website
                    data.lang = lang
                    data.save()

                    if schedule:
                        Content.objects.filter(pk=data.id).update(schedule=schedule, is_schedule=True)

                    return JsonResponse({'success':_('Your post was upload successfully')})
                else:
                    print(form.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/BlogFormVideo.html', { 
                        'form': form,
                        'errors': form.errors,
                        'form_name': form_id
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
        
        if form_id == "BlogFormImage": 
            if pk:
                post=Content.objects.get(pk=pk)
                form = BlogFormImage(request.POST, request.FILES, instance=post)
                website = request.POST.get('website')
                schedule = request.POST.get('schedule')
                if form.is_valid():
                    data = form.save(commit=False)
                    data.author = author
                    data.section = "Blog Post"
                    data.site = website
                    data.lang = lang
                    data.save()

                    if schedule:
                        Content.objects.filter(pk=data.id).update(schedule=schedule, is_schedule=True)

                    return JsonResponse({'success':_('Your post was upload successfully')})
                else:
                    print(form.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/BlogFormImage.html', { 
                        'form': form,
                        'pk': pk,
                        'errors': form.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
            else:
                form = BlogFormImage(request.POST, request.FILES)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.author = author
                    data.section = "Blog Post"
                    data.lang = lang
                    data.save()

                    return JsonResponse({'success':_('Your post was upload successfully')})
                else:
                    print(form.errors)
                    obj_data = render_to_string('stela_control/load-data/maincontent/error_forms/BlogFormImage.html', { 
                        'form': form,
                        'form_name': form_id,
                        'errors': form.errors,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':'content'})
 
def staffData(request):
    if request.method == 'POST':
        lang=request.LANGUAGE_CODE
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        form_name = request.POST.get('form_name')
        pk = request.POST.get('pk')
        print(form_id, action, pk, form_name)

        if action == "checkStaff":   
            if pk:
                staff = Team.objects.get(pk=pk)    
                form = StaffForm(instance=staff)
                get_formset = inlineformset_factory(
                        Team, ProfileGallery, 
                        form=StaffGalleryForm,
                        extra=0, 
                        can_delete=True,
                        validate_min=True, 
                        min_num=1 
                )
                get_formset2 = inlineformset_factory(
                        Team, SocialLinks, 
                        form=SocialMediaForm,
                        extra=0, 
                        can_delete=True,
                        validate_min=True, 
                        min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/staff/form.html', { 
                        'form': form,
                        'formset': get_formset(prefix='gallery', instance=staff),
                        'formset2': get_formset2(prefix='formset', instance=staff),
                        'pk': pk
                    })
                return JsonResponse({'content': obj_data})
            else:
                form = StaffForm()
                get_formset = inlineformset_factory(
                        Team, ProfileGallery, 
                        form=StaffGalleryForm,
                        extra=0,
                        can_delete=False,
                        validate_min=True, 
                        min_num=1 
                )
                get_formset2 = inlineformset_factory(
                        Team, SocialLinks, 
                        form=SocialMediaForm,
                        extra=0,
                        can_delete=False,
                        validate_min=True, 
                        min_num=1 
                )
                obj_data = render_to_string('stela_control/load-data/staff/form.html', { 
                        'form': form,
                        'formset': get_formset(prefix='gallery'),
                        'formset2': get_formset2(prefix='formset'),
                        'pk': pk
                    })
                return JsonResponse({'empty': obj_data})
        
        if action == "removeStaff":
            pk=request.POST.get('id')
            staff=Team.objects.get(pk=pk)
            staff.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
        if form_id == "staff-form":
            if pk:
                staff = Team.objects.get(pk=pk)
                form = StaffForm(request.POST, request.FILES, instance=staff)
                set_formset = inlineformset_factory(
                    Team, SocialLinks, 
                    form=SocialMediaForm,
                    extra=0, 
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                    )
                set_formset2 = inlineformset_factory(
                    Team, ProfileGallery, 
                    form=StaffGalleryForm,
                    extra=0, 
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                    )
                formset = set_formset(request.POST, request.FILES, prefix='formset', instance=staff)
                formset2 = set_formset2(request.POST, request.FILES, prefix='gallery', instance=staff)    
                if all([form.is_valid(), 
                        formset.is_valid(),
                        formset2.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.owner = request.user
                    parent.lang = lang
                    parent.save()

                    instances = formset.save(commit=False)
                                
                    for obj in formset.deleted_objects:
                            obj.delete()
                                
                    for instance in instances:
                        instance.profile = parent
                        instance.save()
                    
                    instances2 = formset2.save(commit=False)
                                
                    for obj in formset2.deleted_objects:
                            obj.delete()
                                
                    for instance in instances2:
                        instance.parent_staff = parent
                        instance.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/staff/form.html', { 
                        'form': form,
                        'formset': formset,
                        'formset2': formset2,
                        'pk': pk,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                form = StaffForm(request.POST, request.FILES)
                set_formset = inlineformset_factory(
                    Team, SocialLinks, 
                    form=SocialMediaForm,
                    extra=0, 
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                    )
                formset = set_formset(request.POST, request.FILES, prefix='formset')
                    
                if all([form.is_valid(), 
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    parent.owner = request.user
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.parent_staff = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/staff/form.html', { 
                        'form': form,
                        'formset': formset,
                    })
                    return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
                 
def inventoryData(request):
    if request.method == 'POST':
        data=request.POST.get('pk')
        lang=request.LANGUAGE_CODE
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        form_name = request.POST.get('form_name')
        formset_name = request.POST.get('formset_name')
        model_parent = request.POST.get('model_parent')
        model_child = request.POST.get('model_child')
        type = request.POST.get('type')
        cke = request.POST.get('is_cke')
        cke_formset = request.POST.get('is_cke_formset')
        ckeditor = request.POST.get('ckeditor')
        schedule = request.POST.get('schedule')
        formset_ckeditor = request.POST.get('formset_ckeditor')
        print(form_id, type, form_name, formset_name, action, model_parent, model_child, cke, ckeditor, cke_formset, formset_ckeditor)
    
        if form_name:
            form_class = get_form_class_by_name(form_name)
            formset_class = get_form_class_by_name(formset_name)
            class_parent = get_form_class_by_name(model_parent)
            class_child = get_form_class_by_name(model_child)
            if data:
                obj=Inventory.objects.get(pk=data)
                form=form_class(instance=obj)
                get_formset = inlineformset_factory(
                    class_parent, class_child, 
                    form=formset_class,
                    extra=0, 
                    can_delete=True,
                    validate_min=True, 
                    min_num=1 
                )
                if schedule:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(instance=obj, prefix='formset'), 
                        'pk': data,
                        'cke': cke,
                        'cke_formset': cke_formset,
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'schedule': schedule
                    })
                    response = JsonResponse({
                        'content': obj_data,
                        'cke': cke,
                        'schedule': schedule,
                        'is_cke_formset': cke_formset
                        })
                else:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(instance=obj, prefix='formset'), 
                        'pk': data,
                        'cke': cke,
                        'cke_formset': cke_formset,
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({
                        'content': obj_data,
                        'cke': cke,
                        'is_cke_formset': cke_formset
                        })
            else:
                form=form_class()
                get_formset = inlineformset_factory(
                    class_parent, class_child, 
                    form=formset_class,
                    extra=0, 
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                if schedule:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(prefix='formset'), 
                        'cke': cke,
                        'cke_formset': cke_formset,
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'schedule': schedule
                    })
               
                    response = JsonResponse({
                        'empty': obj_data,
                        'cke': cke,
                        'is_cke_formset': cke_formset,
                        'schedule': schedule
                        })
                else:
                    obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': get_formset(prefix='formset'), 
                        'cke': cke,
                        'cke_formset': cke_formset,
                        'type': type,
                        'form_name': form_name,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({
                        'empty': obj_data,
                        'cke': cke,
                        'is_cke_formset': cke_formset,
                    })
                    
            return response

        if form_id:
            products=Variant.objects.all()
            sku_count=products.count() + 1 
            form_class = get_form_class_by_name(form_id)
            formset_class = get_form_class_by_name(formset_name)
            class_parent = get_form_class_by_name(model_parent)
            class_child = get_form_class_by_name(model_child)
            if data:
                service=Inventory.objects.get(pk=data)
                set_formset = inlineformset_factory(
                    class_parent, class_child, 
                    form=formset_class,
                    extra=0, 
                    can_delete=True,
                    )
                form = form_class(request.POST, request.FILES, instance=service)  
                formset = set_formset(request.POST, request.FILES, instance=service, prefix='formset')  
                if all([form.is_valid(), 
                        formset.is_valid(),
                    ]):
                        parent = form.save(commit=False)
                        if type == "Product":
                            cat_id = form.cleaned_data['category']
                            category=Category.objects.get(pk=cat_id.pk)
                            get_code = str(category.type+'-'+category.slug+'-'+str(sku_count))
                            parent = form.save(commit=False)
                            parent.category = category
                            parent.sku = get_code
                        parent.owner = request.user
                        parent.type = type
                        parent.lang = lang
                        parent.save()
                            
                        instances = formset.save(commit=False)
                                
                        for obj in formset.deleted_objects:
                                obj.delete()
                                
                        for instance in instances:
                            instance.parent = parent
                            instance.save()

                        return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    if schedule:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'cke': ckeditor,
                        'cke_formset': cke_formset,
                        'type': type,
                        'pk': data,
                        'form_name': form_id,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'schedule': schedule,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor, 'schedule':schedule, 'is_cke_formset': cke_formset})
                    else:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'cke': ckeditor,
                        'cke_formset': cke_formset,
                        'type': type,
                        'pk': data,
                        'form_name': form_id,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor, 'is_cke_formset': cke_formset})
                
            else:
                form = form_class(request.POST, request.FILES)
                set_formset = inlineformset_factory(
                    class_parent, class_child, 
                    form=formset_class,
                    extra=0, 
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                    )
                formset = set_formset(request.POST, request.FILES, prefix='formset')
                    
                if all([form.is_valid(), 
                        formset.is_valid(),
                    ]):
                    parent = form.save(commit=False)
                    if type == "Product":
                        cat_id = form.cleaned_data['category']
                        category=Category.objects.get(pk=cat_id.pk)
                        get_code = str(category.type+'-'+category.slug+'-'+str(sku_count))
                        parent = form.save(commit=False)
                        parent.category = category
                        parent.sku = get_code
                    parent.owner = request.user
                    parent.type = type
                    parent.lang = lang
                    parent.save()

                    for form in formset:
                        child = form.save(commit=False)
                        child.parent = parent
                        child.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    if schedule:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'cke': ckeditor,
                        'cke_formset': cke_formset,
                        'type': type,
                        'form_name': form_id,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'schedule': schedule,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor, 'schedule':schedule, 'is_cke_formset': cke_formset})
                    
                    else:
                        obj_data = render_to_string('stela_control/load-data/inventory/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'cke': ckeditor,
                        'cke_formset': cke_formset,
                        'type': type,
                        'form_name': form_id,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        })
                        return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke':ckeditor, 'is_cke_formset': cke_formset})
                    
        if action == "deleteObj":
            item_ids = request.POST.getlist('id[]')
            class_parent = get_form_class_by_name(model_parent)
            for id in item_ids:
                obj = class_parent.objects.get(pk=id)
                obj.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
            
def sendgridData(request, id, ig):
    ig_account=InstagramAccount.objects.get(asset_id=ig)
    if request.method == 'POST':
        action = request.POST.get('form-id')
        lang=request.LANGUAGE_CODE
        call = request.POST.get('action')
        print(action)
        print(call)

        if action == "sendgrid-form":
            site_cookie=SiteData(request)
            form = SendGridForm(request.POST)
            if form.is_valid():
                html_content = render_to_string('stela_control/emails-template/marketing/content-planner-email.html', {
                    'client':form.cleaned_data['client'],
                    'report':form.cleaned_data['message'],
                    'id_page':id,
                    'lang': lang,
                    'id_instagram':ig,
                    'date': timezone.now(),
                    'company': site_cookie.company_public()
                })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            form.cleaned_data['subject'],
                            text_content,
                            settings.STELA_EMAIL,
                            [form.cleaned_data['email']]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return JsonResponse({'success':_('Your content grid was sent successfully')})
            else:
                print(form.errors)
                errors = form.errors.as_json()
                return JsonResponse({'alert': errors})
        
        if action == "sendmetric-form":
            site_cookie=SiteData(request)
            form = SendGridForm(request.POST)
            if form.is_valid():
                html_content = render_to_string('stela_control/emails-template/marketing/content-planner-email.html', {
                    'client':form.cleaned_data['client'],
                    'report':form.cleaned_data['message'],
                    'id_page':id,
                    'lang': lang,
                    'id_instagram':ig,
                    'company': site_cookie.company_public()
                })

                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                            form.cleaned_data['subject'],
                            text_content,
                            settings.STELA_EMAIL,
                            [form.cleaned_data['email']]
                                            
                        )
                email.attach_alternative(html_content, "text/html")
                email.send()
                return JsonResponse({'success':_('Your IG Analyzer was sent successfully')})
            else:
                print(form.errors)
                errors = form.errors.as_json()
                return JsonResponse({'alert': errors})
        
        if call == "loadPages":
            get_timezone = request.POST.get('zone') 
            starts = int(request.POST.get('start'))
            ends = int(request.POST.get('ends'))
            new_posts = IGPost.objects.filter(parent=ig_account).order_by('-schedule')[starts:ends]
            new_pages = render_to_string('stela_control/load-data/meta/ig-new-pages.html', {
                    'newposts': new_posts,
                    'instagram': ig_account,
                    'usertz': get_timezone,
                    })
            return JsonResponse({'response': new_pages})

def bookingData(request):
    if request.method == 'POST':
        owner=UserBase.objects.get(is_superuser=True)
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        print(form_id, action)

        if action == "consulting_appointment":
            form=BookingConsultingForm(request.POST)
            if form.is_valid():
                booking_list = Booking.objects.filter(owner=owner, date=form.cleaned_data['schedule'])
                if booking_list.count() > 10:
                    return JsonResponse({'alert':_('There is no availability for the selected day, please choose another.')})  
                else:
                    data = Booking()
                    data.owner = owner
                    data.name = form.cleaned_data['name']
                    data.address = form.cleaned_data['address']
                    data.email = form.cleaned_data['email']
                    data.type = form.cleaned_data['type']
                    data.date = form.cleaned_data['schedule']
                    data.dateConfirm = True
                    data.save()
                    services = request.POST.getlist('services[]')
                    for service in services:
                        BookingServices.objects.create(
                            parent=data,
                            service=service
                        )
                    return JsonResponse({'success':_('Your appointment has been successfully scheduled.')})  
               
def inputsData(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        field_value = request.POST.get('field_value')
        field_name = request.POST.get('field_name')
        regex_patterns = {
            'name': r'^[a-zA-Z\s]+$',
            'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            'address': r'.+', 
        }

        if action == "validateBillingData":
            
            pattern = regex_patterns.get(field_name)

            if pattern and re.fullmatch(pattern, field_value):

                response = JsonResponse ({'status': 'success'})
            else:
                response = JsonResponse ({
                    'status': 'error',
                    'field': field_name,
                    'message':_('The value entered in the field is not valid.')
                })

            return response

def requestAPI(request): 
    lang=request.LANGUAGE_CODE
    action = request.POST.get('action')
    form_id = request.POST.get('form-id')
    obj = request.POST.get('queryid')
    print(action, form_id)
    if not obj:
        obj = 0

    stelaquery=ProStelaData.objects.filter(pk=obj)
        
    if action == 'callProStelaCustom':
        start_time = time.time()
        prompt_limit= 10
        openai.api_key = settings.API_KEY
        
        prompt = request.POST.get('prompt')

        qtitle=str(prompt)
        string=qtitle.split()
        title=" ".join(string[:8])
        
        if stelaquery.exists():
                text=ProStelaData.objects.get(id=obj)
                messages=ast.literal_eval(text.chatbox)
                storage_data=ast.literal_eval(text.storage_data)
        else:
            messages = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'}
                    ]
            storage_data = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'}
                    ]

        while action != 'end':
            if len(messages) > prompt_limit:
                del messages[6:9]
            messages.append({'role': 'user', 'content': prompt})
            storage_data.append({'role': 'user', 'content': prompt})
            print(len(messages))
            try:
                response = openai.chat.completions.create (
                    model='gpt-3.5-turbo-16k',
                    messages=messages,
                    temperature=0.2
                )
                tokens=response.usage.total_tokens
                response_content = response.choices[0].message.content
                response_content.replace('\n', '<br>')
                    
                if tokens < 4097:
                    messages.append({"role": "assistant", "content":response_content})
                    storage_data.append({"role": "assistant", "content":response_content})

                    
                chat_html = render_to_string('stela_control/load-data/chatbox2.html', {
                    'messages': storage_data,
                    'user': request.user,
                    })
                
                end_time = time.time()
                response_time = end_time - start_time
                print(response_time)

                if stelaquery.exists():
                    stelaquery.update(
                        chatbox=messages, 
                        storage_data=storage_data,
                        response_time=response_time
                    )
                    qs=ProStelaData.objects.get(id=obj)
                else:
                    qs=ProStelaData.objects.create(
                        title=title,
                        user=request.user,
                        section="custom",
                        chatbox=messages,
                        storage_data=storage_data,
                        response_time=response_time
                    )
                ProStelaUsage.objects.create(
                    prompt=qs,
                    tokens=tokens
                )
                if tokens < 4097:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        })
                else:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        'alert1': 'event'
                        })
                
            except openai.APIError as e:
                    return JsonResponse({
                        'alert2': 'event'
                        })
                  
    if action == 'callProStelaContent':
        start_time = time.time()
        prompt_limit= 10
        openai.api_key = settings.API_KEY
        
        prompt = request.POST.get('prompt')

        qtitle=str(prompt)
        string=qtitle.split()
        title=" ".join(string[:8])
        
        if stelaquery.exists():
                text=ProStelaData.objects.get(id=obj)
                messages=ast.literal_eval(text.chatbox)
                storage_data=ast.literal_eval(text.storage_data)
        else:
            messages = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'},
                        {'role': 'system', 'content': 'Eres especialista en redacción de contenido'}
                    ]
            storage_data = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'},
                        {'role': 'system', 'content': 'Eres especialista en redacción de contenido'}
                    ]

        while action != 'end':
            if len(messages) > prompt_limit:
                del messages[6:9]
            messages.append({'role': 'user', 'content': prompt})
            storage_data.append({'role': 'user', 'content': prompt})
            print(len(messages))
            try:
                response = openai.chat.completions.create (
                    model='gpt-3.5-turbo-16k',
                    messages=messages,
                    temperature=0.2
                )
                tokens=response.usage.total_tokens
                response_content = response.choices[0].message.content
                response_content.replace('\n', '<br>')
                    
                if tokens < 4097:
                    messages.append({"role": "assistant", "content":response_content})
                    storage_data.append({"role": "assistant", "content":response_content})

                    
                chat_html = render_to_string('stela_control/load-data/chatbox2.html', {
                    'messages': storage_data,
                    'user': request.user,
                    })
                
                end_time = time.time()
                response_time = end_time - start_time
                print(response_time)

                if stelaquery.exists():
                    stelaquery.update(
                        chatbox=messages, 
                        storage_data=storage_data,
                        response_time=response_time
                    )
                    qs=ProStelaData.objects.get(id=obj)
                else:
                    qs=ProStelaData.objects.create(
                        title=title,
                        user=request.user,
                        section="Content Chats",
                        chatbox=messages,
                        storage_data=storage_data,
                        response_time=response_time
                    )
                ProStelaUsage.objects.create(
                    prompt=qs,
                    tokens=tokens
                )
                if tokens < 4097:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        })
                else:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        'alert1': 'event'
                        })
                
            except openai.APIError as e:
                    print(e)
                    return JsonResponse({
                        'alert2': 'event'
                        })

    if action == 'callProStelaMarketing':
        start_time = time.time()
        prompt_limit= 10
        openai.api_key = settings.API_KEY
        
        prompt = request.POST.get('prompt')

        qtitle=str(prompt)
        string=qtitle.split()
        title=" ".join(string[:8])
        
        if stelaquery.exists():
                text=ProStelaData.objects.get(id=obj)
                messages=ast.literal_eval(text.chatbox)
                storage_data=ast.literal_eval(text.storage_data)
        else:
            messages = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'},
                        {'role': 'system', 'content': 'Eres especialista en marketing'}
                    ]
            storage_data = [{'role': 'system', 'content': 'Me llamo "PRO-Stela AI", una inteligencia artificial muy util, fui diseñada por Daniel Duque director de sistemas y desarrollo experimental de "Emmerut LLC"'}, 
                        {'role': 'system', 'content': 'Emmerut es una empresa Venezolana - Estadounidense fundada por "Leydi Zerpa", "Daniel Duque" y "Carlos Casanova" en 2022 bajo la entidad "Emmerut LLC", trabaja en el sector desarrollo de aplicaciones, servicios cloud e ecommerce, cuentan con soluciones integrales de alto nivel para el desarrollo de startups'},
                        {'role': 'system', 'content': 'Stela Control Dynamic es un administrador de contenido web para manejar y customizar proyectos de desarrollo y facilitar datos financieros para un mejor uso administrativo. Cuenta con 8 modulos "Comunicaciones", "Contenido", "Marketing", "Inventario", "Finanzas", "Operaciones" y "Control de Usuarios"'},
                        {'role': 'system', 'content': '"Leydi Zerpa" es fundadora de la Empresa "Emmerut LLC" nació el 28 de Junio de 1984 en Venezuela, es licenciada en Comercio Internacional egresada de la universidad "Alejandro Humboldt" en Venezuela y actualmente ocupa el cargo de Gerente General de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Daniel Duque" es fundador de la Empresa "Emmerut LLC" nació el 16 de Noviembre de 1989 en Venezuela, es el creador de "Stela Control Dynamic" desarrollador senior full stack y arquitecto cloud, actualmente ocupa el cargo de director de sistemas y desarrollo experimental de "Emmerut LLC"'},
                        {'role': 'system', 'content': '"Carlos Casanova" es fundador de la Empresa "Emmerut LLC" nació el 01 de Agosto de 1995 en Venezuela, reside en los Estados Unidos y actualmente ocupa el cargo de CEO en "Emmerut LLC"'},
                        {'role': 'system', 'content': 'Eres especialista en marketing'}
                    ]

        while action != 'end':
            if len(messages) > prompt_limit:
                del messages[6:9]
            messages.append({'role': 'user', 'content': prompt})
            storage_data.append({'role': 'user', 'content': prompt})
            print(len(messages))
            try:
                response = openai.chat.completions.create (
                    model='gpt-3.5-turbo-16k',
                    messages=messages,
                    temperature=0.2
                )
                tokens=response.usage.total_tokens
                response_content = response.choices[0].message.content
                response_content.replace('\n', '<br>')
                    
                if tokens < 4097:
                    messages.append({"role": "assistant", "content":response_content})
                    storage_data.append({"role": "assistant", "content":response_content})

                    
                chat_html = render_to_string('stela_control/load-data/chatbox2.html', {
                    'messages': storage_data,
                    'user': request.user,
                    })
                
                end_time = time.time()
                response_time = end_time - start_time
                print(response_time)

                if stelaquery.exists():
                    stelaquery.update(
                        chatbox=messages, 
                        storage_data=storage_data,
                        response_time=response_time
                    )
                    qs=ProStelaData.objects.get(id=obj)
                else:
                    qs=ProStelaData.objects.create(
                        title=title,
                        user=request.user,
                        section="Marketing Chats",
                        chatbox=messages,
                        storage_data=storage_data,
                        response_time=response_time
                    )
                ProStelaUsage.objects.create(
                    prompt=qs,
                    tokens=tokens
                )
                if tokens < 4097:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        })
                else:
                    return JsonResponse({
                        'response': chat_html, 
                        'qs':qs.pk,
                        'alert1': 'event'
                        })
                
            except openai.APIError as e:
                    return JsonResponse({
                        'alert2': 'event'
                        })
                                 
    if action == 'callStelaSight':
        url = []
        prompt = str(request.POST.get('prompt'))
        qty = int(request.POST.get('qty'))
        openai.api_key = settings.API_KEY
        response = openai.Image.create(
            prompt=prompt,
            n=qty,
            size="512x512"
            )
        for obj in response['data']:
            url.append(obj['url'])
        
        images_html = render_to_string('stela_control/load-data/meta/stela-sight/data.html', {
                        'url': url,
                        })
        return JsonResponse({'success': images_html})
    
    if action == "smartHashtag":
        hashdata = []
        userdata = []
        placesdata = []
        keyword = str(request.POST.get('qs'))
        keyword_findall = ''.join(re.findall(r'\w+', keyword))
        clean_keyword = keyword_findall.lower()
        url = "https://instagram-data12.p.rapidapi.com/search/"

        querystring = {
            "query":clean_keyword
            }

        headers = {
            "X-RapidAPI-Key": settings.KEYHUB,
            "X-RapidAPI-Host": settings.HUBHOST
        }

        response = requests.get(url, headers=headers, params=querystring)

        data = response.json()
        print(data)
        hashtags = data['hashtags'][:5]
        users = data['users'][:5]
       
        for list in hashtags:
            hashdata.append(list['hashtag'])

        for list in users:
            userdata.append(list['user'])

        boost_html = render_to_string('stela_control/load-data/meta/smart-boost/index.html', {
                        'hashtags': hashdata,
                        'users': userdata,
                        })
        return JsonResponse({'success': boost_html})
    
    if action == "callStelaChat":
        start_time = time.time()
        obj = request.POST.get('queryid')
        text=ProStelaData.objects.get(id=obj)
        messages=ast.literal_eval(text.storage_data)
        chat_html = render_to_string('stela_control/load-data/chatbox2.html', {
                'messages': messages,
                'user': request.user,
                })

        return JsonResponse({'response': chat_html, 'qs':text.pk})
    
    if action == "deleteQuery":
        obj = request.POST.get('queryid')
        query=ProStelaData.objects.get(id=obj)
        query.delete()
        
        return JsonResponse({'success': 'response'})
    
    if action == "cityCheck":
        country_id = request.POST.get('country_id')
        cities = City.objects.filter(country_id=country_id)
    
        return render(request, 'stela_control/load-data/city_data.html', {'cities': cities})

    if action == "checkUserTokenForm":
        form=RegistrationForm()
        obj_data = render_to_string('stela_control/load-data/single-form.html', {
            'form': form,    
        })    
        return JsonResponse({'content': obj_data})
        
    if form_id == "newUserToken":
        form=RegistrationForm(request.POST, request.FILES)  
        if form.is_valid():
            usertoken=form.save(commit=False)
            payload = {
                'user_id': usertoken.pk,
                'exp': datetime.datetime.utcnow() + timedelta(days=60), 
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            usertoken.api_token = token
            usertoken.is_active = True
            usertoken.set_password(form.cleaned_data['password1'])
            usertoken.save()
            return JsonResponse({'success':_('API Client was created successfully')})
        else:
            print(form.errors)
            obj_data = render_to_string('stela_control/load-data/registration/forms/register-form.html', { 
                'form': form,
                }
            )
            return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

    if form_id == 'newcomerForm':
            form = CompanyForm(request.POST, request.FILES)
            get_formset = inlineformset_factory(
                Company, SocialLinks, 
                form=SocialMediaForm,
                extra=0, 
                can_delete=False,
            )
            formset = get_formset(request.POST, prefix="formset")
            business = request.POST.get('select-business')
            city_id = request.POST.get('city_legal')

            if all([form.is_valid(),
                    formset.is_valid()
                ]):
                parent = form.save(commit=False)
                parent.owner = request.user
                parent.business = business
                parent.city_legal = City.objects.get(id=city_id)
                parent.lang = lang
                parent.save()

                for form in formset:
                    child = form.save(commit=False)
                    child.parent = parent
                    child.save()

                return JsonResponse({'success': _('Register validated, Welcome.')}) 
            else:
                obj_data = render_to_string(f'stela_control/load-data/newcomer/form.html', { 
                        'newcomerform': form,
                        'formsetmedia': formset, 
                    })
                return JsonResponse({'alert': _(f'Process failed, please check the errors...'), 'formset_html': obj_data})
            
def get_youtube_playlist_videos(request):

    if request.method == 'POST':
        action = request.POST.get('action')
        video_id =request.POST.get('videoID')
        print(action)

        if action == "loadPreview":
            obj_data = render_to_string('stela_control/load-data/youtube/video-preview.html', { 
                'video_id': video_id
            })
            return JsonResponse({'html': obj_data})

def jobApplication(request):
    if request.method == 'POST':        
        form_id = request.POST.get('form-id')
        print(form_id)
        
        if form_id == "job-submit":
            form=JobApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return JsonResponse({'success':_('Your job application has been send successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/job-application/error-form-v1.html', { 
                'form': form,
                }
            )
            return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

def coreHandlers(request):
    if request.method == 'POST':        
        action = request.POST.get('action')
        form_id = request.POST.get('form-id')
        print(action, form_id)
        
        if action == "loadPagesBlog":
            lang=request.LANGUAGE_CODE
            author = UserBase.objects.get(is_superuser=True)
            starts = int(request.POST.get('start'))
            ends = int(request.POST.get('ends'))
            blog_posts = Content.objects.filter(author=author, section="Blog Post", lang=lang)[starts:ends]
            new_pages = render_to_string('stela_control/load-data/handlers/blog/blog-pages.html', {
                    'blog_posts': blog_posts,
                    })
            return JsonResponse({'response': new_pages})

        if form_id == "blog-search":
            q=request.POST.get('search-data')
            blog_posts=Content.objects.filter(title=q)
            if blog_posts:
                new_pages = render_to_string('stela_control/load-data/handlers/blog/blog-pages.html', {
                        'blog_posts': blog_posts
                        })
            else:
                new_pages = render_to_string('stela_control/load-data/handlers/blog/empty-blog.html')
            return JsonResponse({'response': new_pages})
        
        if form_id == "commentForm":
            lang=request.LANGUAGE_CODE
            pk=request.POST.get('pk')
            post=Content.objects.get(pk=pk)
            form=CommentsFormBlog(request.POST)
            if form.is_valid():
                data=form.save(commit=False)
                data.post = post
                data.lang = lang
                data.save()

                return JsonResponse({'success':_('Your comment has been send successfully')})
            else:
                print(form.errors)
                obj_data = render_to_string('stela_control/load-data/form.html', { 
                'form': form,
                }
            )
            return JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

def dynamicForms(request):
     if request.method=='POST':
        lang=request.LANGUAGE_CODE
        data=request.POST.get('pk')
        form_id = request.POST.get('form-id')
        action = request.POST.get('action')
        form_name = request.POST.get('form_name')
        formset_name = request.POST.get('formset_name')
        model_parent = request.POST.get('model_parent')
        model_child = request.POST.get('model_child')
        cke = request.POST.get('cke')
        schedule = request.POST.get('schedule')
        print(form_id, form_name, formset_name, model_parent, model_child, action, cke, schedule, data) 

        if action == "loadBasicForm":
            form_class = get_form_class_by_name(form_name)
            class_parent = get_form_class_by_name(model_parent)
            if data:
                if model_parent == "Company":
                    parent=class_parent.objects.get(owner_id=data)
                else:
                    parent=class_parent.objects.get(pk=data)
                form=form_class(instance=parent)
                if schedule:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', {
                            'form': form,
                            'pk': data,
                            'form_name': form_name,
                            'model_parent': model_parent,
                            'schedule': schedule
                    })
                    response = JsonResponse({'content': obj_data, 'schedule': schedule})
                elif cke:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', {
                            'form': form,
                            'pk': data,
                            'form_name': form_name,
                            'model_parent': model_parent,
                            'cke': cke
                    })
                    response = JsonResponse({'content': obj_data, 'cke': cke})
                elif schedule and cke:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', {
                            'form': form,
                            'pk': data,
                            'form_name': form_name,
                            'model_parent': model_parent,
                            'schedule': schedule,
                            'cke': cke
                    })
                    response = JsonResponse({'content': obj_data, 'schedule': schedule, 'cke': cke})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', {
                            'form': form,
                            'form_name': form_name,
                            'model_parent': model_parent,
                            'pk': data,
                    })
                    response = JsonResponse({'content': obj_data})
            else:
                form=form_class()
                if schedule:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', {
                            'form': form,
                            'pk': data,
                            'form_name': form_name,
                            'model_parent': model_parent,
                            'schedule': schedule
                    })
                    response = JsonResponse({'content': obj_data, 'schedule': schedule})
                elif cke:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', {
                            'form': form,
                            'pk': data,
                            'form_name': form_name,
                            'model_parent': model_parent,
                            'cke': cke
                    })
                    response = JsonResponse({'content': obj_data, 'cke': cke})
                elif cke and schedule:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', {
                            'form': form,
                            'form_name': form_name,
                            'model_parent': model_parent,
                            'pk': data,
                            'schedule': schedule,
                            'cke': cke
                    })
                    response = JsonResponse({'content': obj_data, 'cke': cke, 'schedule': schedule})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', {
                            'form': form,
                            'form_name': form_name,
                            'model_parent': model_parent,
                            'pk': data,
                    })
                    response = JsonResponse({'content': obj_data})

        if action == "dynamicFormset":
            form_class = get_form_class_by_name(form_name)
            formset_class = get_form_class_by_name(formset_name)
            class_parent = get_form_class_by_name(model_parent)
            class_child = get_form_class_by_name(model_child)
            if data:
                if model_parent == "Company":
                    parent=class_parent.objects.get(owner_id=data)
                else:
                    parent=class_parent.objects.get(pk=data)
                form=form_class(instance=parent)
                get_formset = inlineformset_factory(
                     class_parent, class_child, 
                     form=formset_class,
                     extra=0, 
                     can_delete=True,
                     validate_min=True, 
                     min_num=1 
                )
                print(parent)
                formset=get_formset(instance=parent, prefix='formset')
                if schedule:
                    obj_data = render_to_string('stela_control/load-data/dynamic-formset.html', {
                            'form': form,
                            'formset': formset,
                            'pk': data,
                            'form_name': form_name,
                            'formset_name': formset_name,
                            'model_parent': model_parent,
                            'model_child': model_child,
                            'schedule': schedule
                    })
                    response = JsonResponse({'content': obj_data, 'schedule': schedule})
                elif cke:
                    obj_data = render_to_string('stela_control/load-data/dynamic-formset.html', {
                            'form': form,
                            'formset': formset,
                            'pk': data,
                            'form_name': form_name,
                            'formset_name': formset_name,
                            'model_parent': model_parent,
                            'model_child': model_child,
                            'cke': cke
                    })
                    response = JsonResponse({'content': obj_data, 'cke': cke})
                elif schedule and cke:
                    obj_data = render_to_string('stela_control/load-data/dynamic-formset.html', {
                            'form': form,
                            'formset': formset,
                            'pk': data,
                            'form_name': form_name,
                            'formset_name': formset_name,
                            'model_parent': model_parent,
                            'model_child': model_child,
                            'schedule': schedule,
                            'cke': cke
                    })
                    response = JsonResponse({'content': obj_data, 'schedule': schedule, 'cke': cke})
                else:
                    obj_data = render_to_string('stela_control/load-data/dynamic-formset.html', {
                            'form': form,
                            'formset': formset,
                            'form_name': form_name,
                            'formset_name': formset_name,
                            'model_parent': model_parent,
                            'model_child': model_child,
                            'pk': data,
                    })
                    response = JsonResponse({'content': obj_data})
            else:
                form=form_class()
                get_formset = inlineformset_factory(
                     class_parent, class_child, 
                     form=formset_class,
                     extra=0, 
                     can_delete=True,
                     validate_min=True, 
                     min_num=1 
                )
                if schedule:
                    obj_data = render_to_string('stela_control/load-data/dynamic-formset.html', {
                            'form': form,
                            'formset': get_formset(prefix='formset'),
                            'pk': data,
                            'form_name': form_name,
                            'formset_name': formset_name,
                            'model_parent': model_parent,
                            'model_child': model_child,
                            'schedule': schedule
                    })
                    response = JsonResponse({'content': obj_data, 'schedule': schedule})
                elif cke:
                    obj_data = render_to_string('stela_control/load-data/dynamic-formset.html', {
                            'form': form,
                            'formset': get_formset(prefix='formset'),
                            'pk': data,
                            'form_name': form_name,
                            'formset_name': formset_name,
                            'model_parent': model_parent,
                            'model_child': model_child,
                            'cke': cke
                    })
                    response = JsonResponse({'content': obj_data, 'cke': cke})
                elif cke and schedule:
                    obj_data = render_to_string('stela_control/load-data/dynamic-formset.html', {
                            'form': form,
                            'formset': get_formset(prefix='formset'),
                            'form_name': form_name,
                            'formset_name': formset_name,
                            'model_parent': model_parent,
                            'model_child': model_child,
                            'pk': data,
                            'schedule': schedule,
                            'cke': cke
                    })
                    response = JsonResponse({'content': obj_data, 'cke': cke, 'schedule': schedule})
                else:
                    obj_data = render_to_string('stela_control/load-data/dynamic-formset.html', {
                            'form': form,
                            'formset': get_formset(prefix='formset'),
                            'form_name': form_name,
                            'formset_name': formset_name,
                            'model_parent': model_parent,
                            'model_child': model_child,
                            'pk': data,
                    })
                    response = JsonResponse({'content': obj_data})
        
        if action == "loadSingleFormset":
            form_class = get_form_class_by_name(form_name)
            if data:
                class_parent = get_form_class_by_name(model_parent)
                parent=class_parent.objects.get(pk=data)
                form=form_class(instance=parent)
                if schedule:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', {
                            'form': form,
                            'pk': data,
                            'form_name': form_name,
                            'model_parent': model_parent,
                            'schedule': schedule
                    })
                    response = JsonResponse({'content': obj_data, 'schedule': schedule})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', {
                            'form': form,
                            'form_name': form_name,
                            'model_parent': model_parent,
                            'pk': data,
                    })
                    response = JsonResponse({'content': obj_data})
            else:
                get_formset = formset_factory(
                        form=form_class,
                        extra=0,
                        can_delete=False,
                        validate_min=True, 
                        min_num=1 
                    )
                if schedule:
                    obj_data = render_to_string('stela_control/load-data/formset.html', {
                            'formset': get_formset(prefix='formset'),
                            'form_name': form_name,
                            'schedule': schedule,
                        })
                    response = JsonResponse({'empty': obj_data, 'schedule': schedule})
                else:
                    obj_data = render_to_string('stela_control/load-data/formset.html', {
                            'formset': get_formset(prefix='formset'),
                            'form_name': form_name,
                        })
                    response = JsonResponse({'empty': obj_data})
        
        if action == 'deleteObj':
            class_parent = get_form_class_by_name(model_parent)
            item_ids = request.POST.getlist('id[]')
            for id in item_ids:
                obj = class_parent.objects.get(pk=id)
                obj.delete()
            alert = render_to_string('stela_control/load-data/remove-complete.html', {})
            return JsonResponse({'success': alert})
        
        if form_id == "ResourceForm":
            form_class = get_form_class_by_name(form_id)
            if data:
                class_parent = get_form_class_by_name(model_parent)
                instance = class_parent.objects.get(pk=data)
                form = form_class(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    form.save()
                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                        'form': form,
                        'form_name': form_id,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                set_formset = formset_factory(
                    form=form_class,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset = set_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        form.save()
                    response = JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/formset.html', { 
                        'formset': formset,
                        'form_name': form_id,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

        if form_id == "InvoiceForm":
            form_class = get_form_class_by_name(form_id)
            if data:
                class_parent = get_form_class_by_name(model_parent)
                instance = class_parent.objects.get(pk=data)
                form = form_class(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    model=form.save(commit=False)
                    model.user = request.user
                    model.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                        'form': form,
                        'form_name': form_id,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                set_formset = formset_factory(
                    form=form_class,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset = set_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        model=form.save(commit=False)
                        model.user = request.user
                        model.save()
                    response = JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/formset.html', { 
                        'formset': formset,
                        'form_name': form_id,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

        if form_id == "RetentionForm":
            form_class = get_form_class_by_name(form_id)
            if data:
                class_parent = get_form_class_by_name(model_parent)
                instance = class_parent.objects.get(pk=data)
                form = form_class(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    model=form.save(commit=False)
                    model.user = request.user
                    model.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                        'form': form,
                        'form_name': form_id,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                set_formset = formset_factory(
                    form=form_class,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset = set_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        model=form.save(commit=False)
                        model.user = request.user
                        model.save()
                    response = JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/formset.html', { 
                        'formset': formset,
                        'form_name': form_id,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

        if form_id == "BankStatementForm":
            form_class = get_form_class_by_name(form_id)
            if data:
                class_parent = get_form_class_by_name(model_parent)
                instance = class_parent.objects.get(pk=data)
                form = form_class(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    model=form.save(commit=False)
                    model.user = request.user
                    model.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                        'form': form,
                        'form_name': form_id,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                set_formset = formset_factory(
                    form=form_class,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset = set_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        model=form.save(commit=False)
                        model.user = request.user
                        model.save()
                    response = JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/formset.html', { 
                        'formset': formset,
                        'form_name': form_id,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

        if form_id == "TaxReturnForm":
            form_class = get_form_class_by_name(form_id)
            if data:
                class_parent = get_form_class_by_name(model_parent)
                instance = class_parent.objects.get(pk=data)
                form = form_class(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    model=form.save(commit=False)
                    model.owner = request.user
                    model.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                        'form': form,
                        'form_name': form_id,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
            else:
                set_formset = formset_factory(
                    form=form_class,
                    extra=0,
                    can_delete=False,
                    validate_min=True, 
                    min_num=1 
                )
                formset = set_formset(request.POST, request.FILES, prefix='formset')
                if formset.is_valid():
                    for form in formset:
                        model=form.save(commit=False)
                        model.user = request.user
                        model.save()
                    response = JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/formset.html', { 
                        'formset': formset,
                        'form_name': form_id,
                        'model_parent': model_parent,
                        'model_child': model_child,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})

        if form_id == "SupportForm":
            if data:
                instance = Support.objects.get(pk=data)
                form = SupportForm(request.POST, request.FILES, instance=instance)
                if form.is_valid():
                    model=form.save(commit=False)
                    model.user = request.user
                    model.save()

                    subject = _('Support Case Created')
                    html_content = render_to_string('email_template/transactional/email-template.html', {
                        'title': _("Your case has been created"),
                        'content': _("We will soon respond to your request.")
                    })
                    text_content = strip_tags(html_content)

                    email = EmailMultiAlternatives(
                        subject,
                        text_content,
                        settings.SUPPORT_EMAIL,
                        [parent.email]
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send()

                    return JsonResponse({'success':_('Your case was send successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                        'form': form,
                        'form_name': form_id,
                        'model_parent': model_parent,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke': 'cke_content_toolbar'})
            else:
                form = SupportForm(request.POST, request.FILES)
                if form.is_valid():
                    model=form.save(commit=False)
                    model.user = request.user
                    model.save()
                    return JsonResponse({'success':_('Your case was send successfully')})
                else:
                    print(form.errors)
                    obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                        'form': form,
                        'form_name': form_id,
                        'model_parent': model_parent,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke': 'cke_content_toolbar'})

        if form_id == "MasterSupportForm":
            class_parent = get_form_class_by_name(model_parent)     
            if data:
                instance = class_parent.objects.get(pk=data)
                form = MasterSupportForm(request.POST, instance=instance)
                form2 = ChatSupportForm(request.POST)
                if all([form.is_valid(), 
                        form2.is_valid(),
                    ]):
                    parent=form.save(commit=False)
                    parent.save()

                    child=form2.save(commit=False)
                    if form2.cleaned_data['content'] == '':
                        pass
                        response = JsonResponse({'success':_('Your message was upload successfully')})
                    else:
                        child.case = parent
                        child.superuser = request.user
                        child.save()

                    subject = _('Support Message')
                    html_content = render_to_string('email_template/transactional/email-template.html', {
                        'title': _("Your case requires your attention"),
                        'content': _("The status of your case has been updated. If you do not receive a response within 24 hours, it will be resolved automatically.")
                    })
                    text_content = strip_tags(html_content)

                    email = EmailMultiAlternatives(
                        subject,
                        text_content,
                        settings.SUPPORT_EMAIL,
                        [parent.email]
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send()
                    
                    response = JsonResponse({'success':_('Your message was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                        'form': form2,
                        'form_name': 'MasterSupportForm',
                        'model_parent': model_parent,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke': 'cke_support'})
        
        if form_id == "UserSupportForm":
            class_parent = get_form_class_by_name(model_parent)     
            if data:
                instance = class_parent.objects.get(pk=data)
                form = ChatSupportForm(request.POST, instance=instance)
                form2 = ChatSupportForm(request.POST)
                if all([form.is_valid(), 
                        form2.is_valid(),
                    ]):
                    parent=form.save(commit=False)
                    parent.save()

                    child=form2.save(commit=False)
                    if form2.cleaned_data['content'] == '':
                        pass
                        response = JsonResponse({'success':_('Your message was upload successfully')})
                    else:
                        child.case = parent
                        child.user = request.user
                        child.save()

                    subject = _('Support Message Send')
                    html_content = render_to_string('email_template/transactional/email-template.html', {
                        'title': _("Your message has been sended"),
                        'content': _("We will soon respond to your request.")
                    })
                    text_content = strip_tags(html_content)

                    email = EmailMultiAlternatives(
                        subject,
                        text_content,
                        settings.SUPPORT_EMAIL,
                        [parent.email]
                    )
                    email.attach_alternative(html_content, "text/html")
                    email.send()

                    response = JsonResponse({'success':_('Your message was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                        'form': form2,
                        'form_name': 'UserSupportForm',
                        'model_parent': model_parent,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke': 'cke_support'})
        
        if form_id == "ReviewsForm":
            form_class = get_form_class_by_name(form_id)
            form = form_class(request.POST)
            if form.is_valid():
                model=form.save(commit=False)
                model.user = request.user
                model.save()

                return JsonResponse({'success':_('Your content was upload successfully')})
            else:
                obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                    'form': form,
                    'form_name': form_id,
                })
                response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke': 'cke_content_toolbar'})  
        
        if form_id == "MasterReviewsForm":
            class_parent = get_form_class_by_name(model_parent) 
            if data:
                instance = class_parent.objects.get(pk=data)
                form_class = get_form_class_by_name(form_id)
                form = form_class(request.POST, instance=instance)
                if form.is_valid():
                    form.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                        'form': form,
                        'form_name': form_id,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke': 'cke_content'})  

        if form_id == "MasterCommentsFormBlog":
            class_parent = get_form_class_by_name(model_parent) 
            if data:
                instance = class_parent.objects.get(pk=data)
                form_class = get_form_class_by_name(form_id)
                form = form_class(request.POST, instance=instance)
                if form.is_valid():
                    form.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                        'form': form,
                        'form_name': form_id,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke': 'cke_message'})  

        if form_id == "MasterContactForm":
            class_parent = get_form_class_by_name(model_parent) 
            if data:
                instance = class_parent.objects.get(pk=data)
                form_class = get_form_class_by_name(form_id)
                form = form_class(request.POST, instance=instance)
                if form.is_valid():
                    form.save()

                    return JsonResponse({'success':_('Your content was upload successfully')})
                else:
                    obj_data = render_to_string('stela_control/load-data/single-form.html', { 
                        'form': form,
                        'form_name': form_id,
                    })
                    response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke': 'cke_message'})  
        
        if form_id == "EditCompanyForm":
            pk=request.POST.get('pk')
            ckeditor=request.POST.get('ckeditor')
            parent=Company.objects.get(owner_id=pk)
            form = EditCompanyForm(request.POST, request.FILES, instance=parent)
            get_formset = inlineformset_factory(
                Company, SocialLinks, 
                form=SocialMediaForm,
                extra=0, 
                can_delete=True,
                validate_min=True, 
                min_num=0 
            )
            formset = get_formset(request.POST, prefix="formset", instance=parent)
            if all([form.is_valid(),
                    formset.is_valid()
                ]):
                parent = form.save(commit=False)
                parent.save()

                instances = formset.save(commit=False)
            
                for obj in formset.deleted_objects:
                        obj.delete()
                            
                for instance in instances:
                    instance.parent_company = parent
                    instance.save()
                    
                response = JsonResponse({'success':_('Your content was upload successfully')})
            else:
                print(form.errors)
                print(formset.errors)
                obj_data = render_to_string('stela_control/load-data/dynamic-formset.html', { 
                    'form': form,
                    'formset': formset,
                    'form_name': form_id,
                    'formset_name': formset_name,
                    'model_parent': model_parent,
                    'model_child': model_child,
                    'cke': ckeditor,
                    'pk': pk
                })
                response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data, 'cke': 'cke_message'})  
        
        if form_id == "UserEditForm":
            pk=request.POST.get('pk')
            obj=UserBase.objects.get(pk=pk)
            form=UserEditForm(request.POST, request.FILES, instance=obj) 
            get_formset = inlineformset_factory(
                    UserBase, SocialLinks, 
                    form=SocialMediaForm,
                    extra=0, 
                    can_delete=True,
                    validate_min=True, 
                    min_num=0
                )
            formset=get_formset(request.POST, prefix='formset', instance=obj)
            if all([form.is_valid(), 
                    formset.is_valid(),
                    ]):
                parent_user = form.save(commit=False)
                parent_user.save()
                
                instances = formset.save(commit=False)
                for obj in formset.deleted_objects:
                    obj.delete()
                                
                for form in instances:
                    form.parent_user = parent_user
                    form.save()

                response = JsonResponse({'success':_('Your profile has been updated')})  
            else:
                obj_data = render_to_string('stela_control/load-data/dynamic-formset.html', { 
                        'form': form,
                        'formset': formset,
                        'form_name': form_id,
                        'formset_name': formset_name,
                        'model_parent': model_parent,
                        'model_child': model_child,
                        'pk': pk
                    })
                response = JsonResponse({'alert': _('Process failed, please check the errors...'), 'formset_html': obj_data})
        
        return response

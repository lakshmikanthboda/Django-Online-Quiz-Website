from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from .models import register, questions,post,comment,quizquestions,quizes,results,Transaction
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction
from django.conf import settings
import datetime
from .paytm import generate_checksum, verify_checksum





op = ''


def execute(data, args):
    import subprocess
    global op
    op = ''
    file = 'file.py'
    f = data
    count = (f.count('input'))
    for i in range(f.count('input')):
        f = f.replace('input', "sys.argv[" + str(i + 1) + ']' + '#')

    if count > 0:
        with open(file, 'w') as w:
            f = 'import sys\n' + f
            w.write(f)
        # print(['python',file,args])
        proc = subprocess.Popen(['python', file, args], stdout=subprocess.PIPE, universal_newlines=True,
                                stderr=subprocess.PIPE, shell=True)
        op = str(proc.communicate()[0]).strip()
        print(op)
    else:
        with open(file, 'w') as w:
            w.write(data)
            w.save()
            w.close()
        print(['python', file, args])
        proc = subprocess.Popen(['python', file, args], stdout=subprocess.PIPE, universal_newlines=True,
                                stderr=subprocess.PIPE, shell=True)
        op = str(proc.communicate()[0]).strip()
        print(op)






# Create your views here.

def check(c, i, l):
    global op
    import requests, json
    result_url = 'https://ide.geeksforgeeks.org/submissionResult.php'
    url = 'https://ide.geeksforgeeks.org/main.php'

    program = c
    inputs = i
    data = {
        'lang': l,
        'code': program,
        'input': inputs,
        'save': 'false'
    }
    r = requests.post(url=url, data=data)
    try:
        p = json.loads(r.text)['sid']
    except:
        op = 'Unknown Error'
        return 0

    data = {'sid': p,
            'requestType': 'fetchResults'}
    while 1:
        result = requests.post(url=result_url, data=data)

        if 'SUCCESS' in result.text:
            r = json.loads(result.text)
            try:
                op = r['output']
                break

            except:
                if 'rntError' in result.text:
                    r = json.loads(result.text)
                    op = 'Error ' + r['rntError']
                break


def index(request):
    global op
    if request.method == "POST":
        code = str(request.POST['code']).strip()
        ip = str(request.POST['input']).strip()
        lan = str(request.POST['lan']).strip()
        print(code, ip, lan)
        execute(code,ip)
        #check(code, ip, lan)
        return render(request, 'compiler.html', {'op': op, 'ip': ip, 'code': code})
    else:
        return render(request, 'compiler.html', {'op': 'Output', 'ip': 'Inputs', 'code': 'Your Code here'})


def home(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def blog(request):
    return render(request, 'blog.html')


def registeruser(request):
    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        password = request.POST['password']
        if name != ' ' and email != '' and mobile != '' and password != '':
            data = register.objects.all()
            emails = []
            for d in data:
                emails.append(d.email)
            usernames=[]
            for i in User.objects.all():
                usernames.append(i.username)
            if email not in emails and name not in usernames:
                user= User.objects.create_user(username=name, email=email, password=password,first_name=name,last_name=name)
                user.save()
                registe = register(name=name, email=email, mobile=mobile, password=password, answers=0, answered=[0])
                registe.save()
                message = 'Registation Succesful'
            else:
                message = 'UserName or Email already registered'
        else:

            message = 'Fill all Details'
        return render(request, 'index.html', {'message': message})
    else:
        message = False
        return render(request, 'index.html', {'message': message,'questions':len(questions.objects.all()),'students':len(register.objects.all())})


def login(request):
    email = request.POST['email']
    password = request.POST['password']
    if email != '' and password != " ":
        d=register.objects.filter(email=email)
        data = register.objects.all()
        print(email,password)
        user = auth.authenticate(username=email.strip(),password=password.strip())
        print(user)
        if user is not None:
            auth.login(request,user)
            message = 'Login Succesful'
            return redirect('/quiz')
        else:
            message = 'Login Failed'
    else:
        message = 'Fill all Details'

    return render(request, 'index.html', {'message': message})


def test(request):
    global name
    try:
        name = request.POST['email']
    except:
        name = ''
    t = register.objects.get(email=name)
    i = str(int(t.answers) + 1)
    global op
    try:
        questio = questions.objects.get(id=i)
    except:
        return render(request,'congo.html',{'user':t.name,'email':name})
    if request.method == "POST":
        try:
            code = str(request.POST['code']).strip()
            ip = str(request.POST['input']).strip()
            lan = str(request.POST['lan']).strip()
            #check(code, ip, lan)
            execute(code,ip)

            print(op)
            if questio.answer.strip() == op.strip():
                t = register.objects.get(email=name)
                ans = t.answered
                if str(i) not in str(ans):
                    t.answers = str(int(t.answers) + 1)
                    ans = ans + ' ' + str(i)
                    t.answered = ans
                    t.save()
                return render(request, 'compiler.html',
                              {'op': op, 'ip': ip, 'code': code, 'succes': True, 'user': name,'next':True,'question': questio.question})
        except:
            t = questions.objects.get(no=i)
            op = t.answer
            ip = t.inputs
            code = ''
            return render(request, 'compiler.html', {'op': op, 'ip': ip, 'code': code, 'succes': False, 'user': name,'question': questio.question})

        else:
            return render(request, 'compiler.html', {'op': op, 'ip': ip, 'code': code, 'succes': False, 'user': name,'question': questio.question})

    else:
        questio = questions.objects.all()
        # print(questio[i].question)
        return render(request, 'compiler.html',
                      {'op': questio.answer, 'ip': questio[i].inputs, 'code': 'Your Code here',
                       'question': questio.question, 'user': name})
def gg(request):
    posts1=(post.objects.all()[0:len(post.objects.all())/2])[::-1]
    posts2 = (post.objects.all()[len(post.objects.all()) / 2:])[::-1]
    return render(request,'test.html',{'posts1':posts2,'a':'0','posts2':posts1})

def show(request,pk):
    g=post.objects.get(id=pk)
    return render(request,'blog-single.html',{'img':g.img.url,'content':g.content,'title':g.title,'cat':g.cat,'date':g.date})

def team(request):
    return render(request,'teachers.html')

def contact(request):
    if request.method=="POST":

        fname=request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        comments = request.POST['comments']
        if fname!=''and lname != '' and email != '' and phone != '' and comments != '':
            registe = comment(fname=fname,lname=lname,email=email,phone=phone,comments=comments)
            registe.save()
            sent=True
            message=' Message Sent Succesfully'
            return render(request,'contact.html',{'sent':sent,'message':message})
        else:
            sent = True
            message = 'Fill all Details'
            return render(request, 'contact.html', {'sent': sent, 'message': message})

    else:
        return render(request,'contact.html')
def quizhome(request,id,uid):
    if not(request.user.is_active):
        return HttpResponse('Please Login to Continue')
    try:
        g=quizes.objects.get(id=id)
        u=User.objects.get(id=uid)
    except:
        return redirect('/')
    if u in g.users.all():
        if u not in g.completed.all():
            if request.user.is_active and str(request.user.id).strip() == str(uid).strip():
                g.completed.add(u)
                time=g.time
                print(g.title)
                q=quizquestions.objects.filter(quiz=id)
                return render(request,'quiz.html',{'time':time,'questions':q,'id':id})
            else:
                return HttpResponse('Log in to continue')
        else:
            if request.user.is_active and str(request.user.id).strip() == str(uid).strip():
                r=quizes.objects.get(id=id)
                r=(r.reult.split('\n'))[1:-1]
                a=[]
                for rr in r:
                    rr=rr.replace(',','_____')
                    a.append(rr)

                return render(request,'result.html',{'d':a})
            else:
                return HttpResponse('Login First')
    else:
        id=str(id)
        uid=str(uid)
        q=quizes.objects.get(id=id)
        if request.user.is_active and str(request.user.id).strip() == uid.strip():
            if q.amount>0:
                return render(request,'paymentstarter.html',{'id':id,'uid':uid,'amount':q.amount})
            else:
                g.users.add(u)
                g.save()
                return redirect('/quiz')
        else:
            return HttpResponse('Login First')
def logout(request):
    auth.logout(request)
    return redirect('/')
def answers(request):
    qid=request.POST['qid']
    uid=request.POST['uid']
    answrs=quizquestions.objects.filter(quiz=qid)
    count=0
    for i in range(len(answrs)):
        try:
            if answrs[i].answer.strip()==request.POST[str(i+1)].strip():
                count+=1
        except:
            pass
    r=quizes.objects.get(id=qid)
    p=User.objects.get(id=uid)
    r.reult+='\n'+str(uid)+','+str(p.username)+','+str(p.email)+','+str(count)+'\n'
    r.save()
    return redirect('/quiz')

def quiz(request):
    if request.user.is_active:
        q=quizes.objects.filter(status=True ,end=False)
        e=quizes.objects.filter(end=True, status=True)
        return render(request,'quizhome.html',{'q':q[::-1],'e':e[::-1]})
    else:
        return HttpResponse('Log in to see')
def test2(request):
    g=quizes.objects.all()
    print(g[0].title)
    print(g[0].time)
    print(g[0].users.all())
    print('lk' in g[0].users.all())
    return render(request,'tst.html',{'a':g[0]})

def initiate_payment(request):
    if request.method == "GET":
        return render(request, 'pay.html')
    try:
        uid = request.POST['uid']
        qid = request.POST['qid']
        amount = int(request.POST['amount'])
    except:
        return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})
    u=User.objects.get(id=uid)
    transaction = Transaction.objects.create(made_by=u, amount=amount,qid=qid,uid=uid,made_on=datetime.datetime.now())
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    import time
    time.sleep(3)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)

        paytm_params = {}

        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            if received_data['RESPCODE'][0]=='01':
                g=Transaction.objects.filter(order_id=received_data['ORDERID'][0])
                q=quizes.objects.get(id=g[0].qid)
                q.users.add(g[0].uid)
                q.save()
                g[0].status=True
                g[0].save()
                #q=quizes.objects.get(id=received_data['QID'])
                #q.users.add(User.objects.get(id=received_data['UID']))
                received_data['message'] = "Checksum Matched"
            else:
                return HttpResponse('Payment Failed <meta http-equiv="refresh" content="2;url=quiz" />')
        else:
            received_data['message'] = "Checksum Mismatched"
        return render(request, 'callback.html', context=received_data)
from datetime import datetime
from django.contrib.auth.models import User, auth
from django.db import models
from django.utils import timezone
class register(models.Model):
    name= models.CharField(max_length=153)
    email=models.EmailField(max_length=201)
    mobile=models.IntegerField()
    password=models.CharField(max_length=51)
    answers=models.IntegerField()
    answered=models.CharField(max_length=10000)
    def __str__(self):

        return self.name

    class Meta:
        db_table=''
        managed=True
        verbose_name='register'
        verbose_name_plural='registers'

class questions(models.Model):
    question= models.TextField(max_length=1000)
    inputs=models.TextField(max_length=502)
    answer=models.TextField(max_length=501)
    no = models.TextField(max_length=500)
    def __str__(self):
        return str(self.no)

    class Meta:
        db_table=''
        managed=True
        verbose_name='questions'
        verbose_name_plural='questionss'


class post(models.Model):
    title= models.CharField(max_length=300)
    img=models.ImageField(upload_to ='images/')
    cat=models.CharField(max_length=150)
    date = models.DateField(default=timezone.now)
    content=models.TextField()
    def __str__(self):
        return str(self.title)

    class Meta:
        db_table=''
        managed=True
        verbose_name='post'
        verbose_name_plural='posts'

class quizes(models.Model):
    title= models.CharField(max_length=300,unique=True)
    time=models.IntegerField()
    amount = models.IntegerField()
    disc=models.TextField()
    users=models.ManyToManyField(User,related_name='users')
    completed = models.ManyToManyField(User,related_name='completed')
    reult=models.TextField()
    status=models.BooleanField(default=False)
    end = models.BooleanField(default=False)
    def __str__(self):
        return str(self.title)

    class Meta:
        db_table=''
        managed=True
        verbose_name='quiz'
        verbose_name_plural='quizes'

class quizquestions(models.Model):
    quiz=models.ForeignKey(quizes,on_delete=models.CASCADE)
    title= models.CharField(max_length=1000)
    option1=models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    def __str__(self):
        return self.title+' | '+self.answer

    class Meta:
        db_table=''
        managed=True
        verbose_name='question'
        verbose_name_plural='questions'


class results(models.Model):
    quiz=models.ForeignKey(quizes,on_delete=models.CASCADE)
    res= models.TextField()
    def __str__(self):
        return str(self.quiz)

    class Meta:
        db_table=''
        managed=True
        verbose_name='result'
        verbose_name_plural='results'






# Create your models here.
class comment(models.Model):
    fname = models.CharField(max_length=300)
    lname = models.CharField(max_length=300)
    email = models.CharField(max_length=300)
    phone = models.CharField(max_length=300)
    comments = models.TextField()
    def __str__(self):
        return str(self.fname+' | '+self.lname+' | '+self.comments)

    class Meta:
        db_table=''
        managed=True
        verbose_name='comment'
        verbose_name_plural='comments'

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    qid = models.IntegerField()
    uid=models.IntegerField()
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)
    status=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
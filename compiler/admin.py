from django.contrib import admin
from .models import register,questions,post,comment,quizes,quizquestions,results,Transaction

# Register your models here.
admin.site.register(register)
admin.site.register(questions)
admin.site.register(post)
admin.site.register(comment)
admin.site.register(quizes)
admin.site.register(quizquestions)
admin.site.register(results)
admin.site.register(Transaction)
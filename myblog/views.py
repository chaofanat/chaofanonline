from django.shortcuts import render, HttpResponse
from myblog.models import Blog,Contact,FeaturedBlog,Category,Tag
import math

# Create your views here.
def index(request):
    #趋势：博客按阅读量排序取前5
    trend =  Blog.objects.all().order_by('-views')[:5]
    featuredblog = FeaturedBlog.objects.all()
    all_normal_featuredblog = FeaturedBlog.objects.filter(type='all-normal')
    
    tag = Tag.objects.all()
    categorytop = FeaturedBlog.objects.filter(type='category-top').order_by('blog__category')
    categorynormal = FeaturedBlog.objects.filter(type='category-normal').order_by('blog__category')
    category = categorytop.values('blog__category').distinct()
    categoryblog = {}
    for c in category:
        categoryblog[c['blog__category']] = categorynormal.filter(blog__category=c['blog__category'])
    
    result={'featuredblog': featuredblog,'Category': category, 'Tag': tag,'TrendBlog': trend,'CategoryBlog': categoryblog,'CategoryTop': categorytop,'all_normal_featuredblog': all_normal_featuredblog}
    return render(request, 'myblog/index.html', result)


def single_post(request,id=None):
    if id:
        data = Blog.objects.filter(id=id)
        data.update(views=data[0].views+1)
        data = data[0]
        data.save()
    else :
        data = Blog.objects.all().order_by('-time')[0]
    
    trend =  Blog.objects.all().order_by('-views')[:5]
    latest = Blog.objects.all().order_by('-time')[:5]
    tag = Tag.objects.all()
    category = Category.objects.all()
    
    result={'blog': data,'TrendBlog': trend,'LatestBlog': latest,'Tag': tag,'Category': category}
    return render(request, 'myblog/single-post.html', result)


def category(request,page=1,categoryid=None):
    no_of_post=5
    
    
    page=int(page)

    if categoryid:
        blog = Blog.objects.filter(category_id=categoryid)
        category = Category.objects.filter(id=categoryid)[0]
        
    else :
        category = Category.objects.all()[0]
        blog = Blog.objects.filter(category=category)


    length=len(blog)
    no_of_page=math.ceil(length/no_of_post)
    blog=blog[(page-1)*no_of_post: page*no_of_post]
    if page>1:
        prev=page-1
    else:
        prev=None

    if page<math.ceil(length/no_of_post):
        nxt= page+1

    else:
        nxt=None
   

    trend =  Blog.objects.filter(category=category).order_by('-views')[:5]
    latest = Blog.objects.filter(category=category).order_by('-time')[:5]
    categories = Category.objects.all()
    tag = Tag.objects.all()

    result={'blog': blog, 'prev': prev, 'nxt': nxt, 'no_of_page': list(range(1,no_of_page+1)),
              'pagenumber': page,'Category': category,'TrendBlog': trend,'LatestBlog': latest,
            'categories': categories,'Tag': tag,
            }
    return render(request, 'myblog/category.html', result)

def tag(request,page=1,tagid=None):
    no_of_post=5

    page=int(page)

    if tagid:
        blog = Blog.objects.filter(tags__id=tagid)
        tag = Tag.objects.filter(id=tagid)[0]
        
    else :
        tag = Tag.objects.all()[0]
        blog = Blog.objects.filter(tags=tag)
    
    length=len(blog)
    no_of_page=math.ceil(length/no_of_post)
    blog=blog[(page-1)*no_of_post: page*no_of_post]
    if page>1:
        prev=page-1
    else:
        prev=None
    
    if page<math.ceil(length/no_of_post):
        nxt= page+1
    else:
        nxt=None
    
    trend =  Blog.objects.filter(tags=tag).order_by('-views')[:5]
    latest = Blog.objects.filter(tags=tag).order_by('-time')[:5]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    result={'blog': blog, 'prev': prev, 'nxt': nxt, 'no_of_page': list(range(1,no_of_page+1)),
            'pagenumber': page,'Tag': tag,'TrendBlog': trend,'LatestBlog': latest,'Tags': tags,
            'categories': categories,
            }
    return render(request, 'myblog/tag.html', result)


def about(request):
    return render(request,'myblog/about.html')


def blogpost(request, slug):
    blogs = Blog.objects.filter(slug=slug).first()
    context_dict= {'blogs': blogs}
    return render(request, 'blogpost.html', context_dict)
    
   

def contact(request):

    context={'success':False}
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        message=request.POST['message']
        ins=Contact(name=name, email=email, message=message)
        ins.save()
        context={'success':True}

    


    return render(request, 'myblog/contact.html', context)


def search(request):
    return render(request, 'myblog/search-post.html')

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Listing, Watchlist, Bid, Comments


def index(request):
    listings = [listing for listing in Listing.objects.all() if listing.is_active]
    return render(request, "auctions/index.html", {
        "listing": listings,
        'type': 'Active Listings'
    })

def closed_listing_view(request):
    closed_listing = [listing for listing in Listing.objects.all() if not listing.is_active]
    current_user = request.user
    
    winner = []
    for listing in closed_listing:
        highest_bid = Bid.objects.filter(listing_id=listing).order_by('-bid').first()
        if highest_bid and highest_bid.user_id == current_user:
            winner.append(listing)

    return render(request, "auctions/index.html", {
        "listing": closed_listing,
        'type': 'Closed Listings',
        'winner': winner
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def listing_view(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    check = False
    for w_listing in Watchlist.objects.all():
        if w_listing.listing.id == listing_id:
            check = True
    if check: watchlist = 'Remove from watchlist'
    else: watchlist = 'Add in watchlist'
    bidding_details = ''

    if request.method == 'POST':
        if 'close_bid' in request.POST:
            listing.is_active = False
            listing.save()            

        if 'place_bid' in request.POST:
            try:
                bid = int(request.POST.get("bid"))
                if bid <= listing.price:
                    raise ValueError
                else:
                    new_bid = Bid(bid=bid, listing_id=Listing(pk=listing_id), user_id=request.user)
                    new_bid.save()
                    listing.price = bid
                    listing.save()
                    bidding_details = 'Bid transacted successfully'
            except (ValueError, TypeError):
                bidding_details = 'Bid must be greater than current bid'
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    'watchlist': watchlist,
                    'message': bidding_details,
                })
        
        if 'comment' in request.POST:
            comment = request.POST.get('comment_text')
            if len(comment) > 0:
                comment_instance = Comments(listing_id=listing, user_id=request.user, comment=comment)
                comment_instance.save()

    winner = False
    if not listing.is_active:
        highest_bid = Bid.objects.filter(listing_id=listing).order_by('-bid').first()
        if highest_bid and highest_bid.user_id == request.user:
            winner = True

    comments = [comment for comment in Comments.objects.all() if comment.listing_id == listing]
    return render(request, "auctions/listing.html", {
            "listing": listing,
            'watchlist': watchlist,
            'message': bidding_details,
            'winner': winner,
            'comments': comments
        })

def create_listing(request, user_id):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        try:
            if request.POST.get('price'):
                price = int(request.POST.get('price'))
            else: price = 0
        except ValueError:
            return render(request, "auctions/create_listing.html", {
                "message": "Invalid price"
            })
        url = request.POST.get('url')
        category = request.POST.get('category')

        if title and description and price != 0:
            listing = Listing(title=title, discription=description, price=price, image_url=url, categories=category, user_id=User(pk=user_id))
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create_listing.html", {
                "message": 'Title, Description or Price is/are empty.'
            })

    return render(request, "auctions/create_listing.html", {})

def watchlist_view(request, listing_id):
    listings = [a_listing.listing for a_listing in Watchlist.objects.all() if a_listing.user == request.user]
    if request.method == "POST":
        watchlists = [watchlisting.listing.id for watchlisting in Watchlist.objects.all()]
        if listing_id not in watchlists:
            listing = Listing.objects.get(pk=listing_id)
            new_watchlist = Watchlist(listing=listing, user=request.user)
            new_watchlist.save()
        else:
            listing = Listing.objects.get(pk=listing_id)
            new_watchlist = Watchlist.objects.get(listing=listing)
            new_watchlist.delete()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    
    return render(request, "auctions/index.html", {
        "listing": listings,
        "type": "Watchlist"
    })

def categories(request):
    categories = set(listing.categories for listing in Listing.objects.all())

    return render(request, "auctions/categories.html", {
    "categories": categories,
    'type': 'Categories'
})

def category_view(request, category):
    listings = [listing for listing in Listing.objects.all() if listing.categories == category]
    return render(request, "auctions/index.html", {
        'type': category,
        'listing': listings
    })
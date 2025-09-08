CS50 Web Programming with Python and JavaScript – Commerce

This is my implementation of **Project 2: Commerce** from Harvard's CS50 Web Programming course.  
The project is an eBay-like e-commerce auction site where users can post listings, place bids, add comments, and manage watchlists.

## Features

User Authentication
	- Register, log in, and log out functionality.	
	- Each user has their own account to manage listings and bids.

Create Listings
	- Authenticated users can create new auction listings.
	- Each listing includes a title, description, starting bid (price), optional image URL, and category.

Active Listings Page
	- Homepage shows all active listings.
	- Each listing displays its current highest bid.

Listing Page
	- Shows details of a specific listing.
	- Authenticated users can:
		- Place a bid (must be higher than the current bid).
		- Add or remove the listing from their personal watchlist.
		- Post comments on the listing.
	- The creator of the listing can close the auction, declaring the highest bidder as the winner.

Watchlist
	- Users can view and manage a personalized watchlist of saved listings.

Categories
	- Users can browse listings filtered by categories.

Comments
	- Users can comment on listings, and comments are displayed under each listing.

Models

- User – extends Django’s `AbstractUser`.
- Listing
  - `title`, `description`, `price`, `image_url`, `date`, `categories`, `is_active`, `user_id`.
- Bid
  - `listing_id`, `user_id`, `bid`, `timestamp`.
- Comments
  - `listing_id`, `user_id`, `comment`, `timestamp`.

---

## How to Run

1. Clone the repository
   ```bash
   git clone <your-repo-url>
   cd commerce

2. Install dependencies
   ```bash
	pip install -r requirements.txt

4. Apply migrations
   ```bash
	python manage.py makemigrations
	python manage.py migrate

5. Create a superuser (optional, for admin access)
   	```bash
	python manage.py createsuperuser

6. Run the development server
   ```bash
	python manage.py runserver

8. Open the site in your browser
	http://localhost:8000

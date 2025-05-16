from sqlalchemy.future import select
from app.database.models import async_session
from app.database.models import Listing, User
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, MultipleResultsFound


async def add_listing(state_data, img_dict):
    async with async_session() as session:
        try:
            # You can add checks here if needed to prevent duplicate listings or other validation
            new_listing = Listing(
                title=state_data['title'].lower(),
                description=state_data['description'],
                price=state_data['price'],
                city=state_data['city'],
                adres=state_data['adres'],
                image1=img_dict.get('image1'),
                image2=img_dict.get('image2'),
                image3=img_dict.get('image3'),
                image4=img_dict.get('image4'),
                image5=img_dict.get('image5'),
                image6=img_dict.get('image6'),
                image7=img_dict.get('image7'),
                image8=img_dict.get('image8'),
                image9=img_dict.get('image9'),
                image10=img_dict.get('image10')
                # image1=image_bytes  # Saving the image as bytes
            )

            session.add(new_listing)
            await session.commit()

            return print("Listing added successfully!")

        except Exception as e:
            # Handle error if something goes wrong
            await session.rollback()  # Rollback changes if any error occurs
            return print(f"Error while adding listing: {str(e)}")


async def get_listings(city):
    async with async_session() as session:
        result = await session.execute(select(Listing).where(Listing.city.ilike(f"{city.lower()}%")))
        # This will return None if no matching row exists.
        listings = result.scalars().all()

    if listings:
        return [(listing.title, listing.description, listing.price, listing.adres, listing.city, listing.image1, listing.image2, listing.image3, listing.image4, listing.image5, listing.image6, listing.image7, listing.image8, listing.image9, listing.image10) for listing in listings]

    else:
        return None


async def get_by_city_price(city, lower, upper):
    async with async_session() as session:
        result = await session.execute(select(Listing).where(Listing.city.ilike(f"{city.lower()}%"),
                                                             Listing.price >= lower,
                                                             Listing.price <= upper))
        listings = result.scalars().all()

    if listings:
        return [(listing.title, listing.description, listing.price, listing.adres, listing.city, listing.image1, listing.image2, listing.image3, listing.image4, listing.image5, listing.image6, listing.image7, listing.image8, listing.image9, listing.image10) for listing in listings]

    else:
        return None


async def get_user(tg_id):
    async with async_session() as session:
        try:
            result = await session.execute(select(User).where(User.telegram_id == tg_id))
            user = result.scalars().all()
            return user
        except NoResultFound:
            print("No user found with the provided Telegram ID.")
            return None
        except MultipleResultsFound:
            return None
            print("Multiple users found with the same Telegram ID.")


async def reg_user(state_data):
    async with async_session() as session:
        try:
            new_user = User(
                name=state_data['name'],
                email=state_data['email'],
                telegram_id=state_data['tg_id']
            )
            session.add(new_user)
            await session.commit()

            return print("User added successfully!")

        except Exception as e:
            # Handle error if something goes wrong
            await session.rollback()  # Rollback changes if any error occurs
            return print(f"Error while adding user: {str(e)}")

# Notes to take During the development of the software

## Dependencies to install
- pip install SQLAlchemy-ImageAttach
- Try to install:
  https://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-on-windows
- pip install sqlalchemy-media
- pip install python-magic-bin==0.4.14
- pip install flask-login
- pip install flask-session
- pip install stripe

## Tests to take
- Test that the user can create an account.
- Test that the user can login with the account
- Test the user can delete the account.
- Test that the password that the user used is the same
- Test that one can retreive the user's attributes
- Test that the place where the picture is going is correct
- Test that the picture is converted to base64 after encoded to bytes
- Test that the picture is converted to image format after it has been decoded to image format
- Test that the user is not an admin
- Test that the user is an admin


# Environmental Variable
CURRENCY_API_KEY api key for currency
STRIPE_SECRET_KEY api key for stripe account


    # im = kwargs.get("image")
    #     for images in im:
    #         if images.get("image_name") in images.keys():
    #             if images.get("image_type") == "covbin":
    #                 image_name = images.get("image_name")
    #                 im = bytes(images.get('image'), 'utf-8')
    #                 with open(image_name, 'rw') as file_name:
    #                     file_name.write(base64.b64decode((im)))
    #                 self.image_list.append(ProductImage.create_from(image_name))
    #             else:
    #                 im = images.get('image')
    #                 self.image_list.append(ProductImage.create_from(im))
    #         else:
    #             info['error']['image_name'] = "Image name is unavaliable"
    #             raise UnavaliableImageName

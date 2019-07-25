from PIL import Image, ImageDraw, ImageFont
import textwrap
import markovify
import random

# OS
import os

# Static
from django.conf import settings

# Useful info:
# 12 capital letters fit into a row of main box
# 15 lowercase letter fit into a row of main box
# 84 capital letter fit into main box


class StarStickerGenerator():
    
    def DrawTextToImage(self, txt, font, font_size, font_colour, max_row_length, coordinates, image):
        """Returns a Boolean

        Crops and draws text to an image. By default it draws comic sans to t
        """
        img = Image.open(image)
        image_to_draw = ImageDraw.Draw(img)
        text_to_draw = textwrap.fill(txt, max_row_length)  # Crop text
        font_type = ImageFont.truetype(font, font_size)
        image_to_draw.text(xy=coordinates, text=text_to_draw, fill=font_colour, font=font_type)
        try:
            img.save(settings.STATIC_IMAGE_FOLDER + '/image_generated.png', 'PNG')
        except Exception as e:
            print("Exception:", e.args[0])
            return False
        finally:
            img.close()
        return True

    def CalculateFontSize(self, txt):
        """Returns int

        Calcuates the appropiate font size. Useful for drawing large text
        """
        txt_length=len(txt)
        res = -46.25614+(79.45031-(-46.25614))/(1+(txt_length/322.0287)**0.4743426)
        return int(res)

    def DrawText(self, txt, font=settings.STATIC_IMAGE_FOLDER + '/fonts/comicbd.ttf', font_colour=(0, 0, 0),
                 max_row_length=20, coordinates=(288, 388), image=settings.STATIC_IMAGE_FOLDER + 'star_template.png'):
        """Returns a Boolean

        By default, it draws text to the star template image. Returns True if the image is saved.
        """
        saved = False
        if txt:
            font_size = self.CalculateFontSize(txt)
            saved = self.DrawTextToImage(txt, font, font_size, font_colour, max_row_length, coordinates, image)
            return saved
        else:
            return saved

    def GenerateSentence(self, state_size=0):
        """Returns string

        Generates a phrase using Markov chains. If state_size is equal to zero, it will be a random int between 1 and 4
        """
        if (state_size < 0):
            return False

        with open(settings.STATIC_IMAGE_FOLDER + 'corpus.txt') as f:
            text = f.read()
            if state_size == 0:
                state_size = random.randint(1,4)
            text_model = markovify.Text(text, state_size)
            for i in range(100):  # tries up to 100 times
                sentence = text_model.make_sentence(tries=100)
                if not sentence:
                    continue
                else:
                    data = {
                        'sentence': sentence,
                        'markov_state': state_size,
                    }
                    return data

    def Generate(self, state_size=0):
        """Main script"""
        data = self.GenerateSentence(state_size)
        saved = self.DrawText(data['sentence'])
        data = {
            'sentence': data['sentence'],
            'markov_state': data['markov_state'],
            'saved': saved,
        }
        if not saved:
            return False
        return data


# EXAMPLE
# a = StarStickerGenerator()
# print("Generated: ", a.Generate())

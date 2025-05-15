from PIL import Image, ImageDraw, ImageFilter, ImageFont
import textwrap
import json

# Load the post data from the JSON file
post_author  = ''
subreddit_title = ''
post_title = ''

with open('assets/inputs/post.json', 'r', encoding='utf-8') as file:
    post = json.load(file)
    post_author = post['author']
    subreddit_title = post['subreddit']
    post_title = post['title']


# Draw the background
img = Image.new('RGBA', (1080, 600), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

lines = textwrap.wrap(post_title, width=40)
font = ImageFont.truetype("assets/fonts/RedditSans-SemiBold.ttf", 48)
x1, y1, x2, y2 = draw.multiline_textbbox((0, 0), '\n'.join(lines), font=font)
post_title_height = y2 - y1

img = img.resize((1080, 24+160+48+post_title_height+48+24))
draw = ImageDraw.Draw(img)

stroke = 4
draw.rounded_rectangle(
    (1, 1, img.size[0]-stroke, img.size[1]-stroke),
    fill=(255, 255, 255),
    outline=(30, 30, 30),
    width=stroke,
    radius=16,
)


# Draw the post title
draw.multiline_text((48, 24+160+48), '\n'.join(lines), font=font, fill=(40, 40, 40, 255))


# Draw the subreddit icon
subreddit = Image.open('assets/inputs/subreddit.png')
background = Image.new('RGBA', subreddit.size, (255, 255, 255, 255))
mask = Image.new("L", subreddit.size, 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, subreddit.size[0], subreddit.size[1]), fill=255)
mask = mask.filter(ImageFilter.GaussianBlur(0))
subreddit = Image.composite(subreddit, background, mask)
draw = ImageDraw.Draw(subreddit)
draw.ellipse((0, 0, subreddit.size[0], subreddit.size[1]), fill=None, outline=(230, 230, 230, 255), width=2)


# Resize the subreddit icon and draw it on the image
subreddit = subreddit.resize((160, 160))
img.paste(subreddit, (32, 32), subreddit)


# Draw the subreddit title
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("assets/fonts/RedditSans-SemiBold.ttf", 40)
draw.text((32+160+24, 32+32), text=f"r/{subreddit_title}", fill=(30, 30, 30, 255), font=font)


# Draw the post author
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("assets/fonts/RedditSans-Regular.ttf", 24)
draw.text((32+160+24, 32+32+40+8), text=post_author, fill=(30, 30, 30, 255), font=font)


# Save the image
img.save('assets/output/thumbnail.png', quality=100)
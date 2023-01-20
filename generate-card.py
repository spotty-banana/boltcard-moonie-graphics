from PIL import Image, ImageDraw, ImageFont
import random
import math
import numpy
from numpy import array

LNPAY_URL = "asdaso8y7hi7fhsaod78fhjoasidfhjolaisdhflias78hdlf78ashdi7fhsdalifosdid"
BALANCE_URL = "8y7hi7fhsaod78fhjoasidfhjolaisdhflias78hdlf78ashdi7fhsdalifosdidasdaso"

def interpolate(f_co, t_co, interval):
    """ interpolate colors (gradient) """
    det_co =[(t - f) / interval for f , t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]

# load pictures
globe = Image.open("Terrestrial_globe.png")
moon = Image.open("moon0.png")
bitcoin_logo_text = Image.open("bitcoin_logo_text.png")

def randomize_colors(img):
    data = array(img)
    colorize_model = random.randint(0, 6)
    for i in range(0, len(data)):
        for j in range(0, len(data[0])):
            if colorize_model == 0:
                data[i][j][0], data[i][j][1] = data[i][j][1], data[i][j][0]
            elif colorize_model == 1:
                data[i][j][0], data[i][j][2] = data[i][j][2], data[i][j][0]
            elif colorize_model == 2:
                data[i][j][1] = data[i][j][0]
            elif colorize_model == 3:
                data[i][j][2] = data[i][j][0]
            elif colorize_model == 4:
                data[i][j][2] = data[i][j][0]
                data[i][j][0], data[i][j][1] = data[i][j][1], data[i][j][0]
            elif colorize_model == 5:
                data[i][j][1] = data[i][j][0]
                data[i][j][0], data[i][j][2] = data[i][j][2], data[i][j][0]
            else:
                pass
    return Image.fromarray(data)


def create_card_graphics():
    background = Image.new('RGBA', globe.size, color=0)

    draw = ImageDraw.Draw(background)

    f_co = (24, 32, 32)
    t_co = (135, 206, 235)
    blue_bottom = 100
    for i, color in enumerate(interpolate(f_co, t_co, background.height-blue_bottom)):
        draw.line([(0, i-blue_bottom), (background.width, i-blue_bottom)], tuple(color), width=1)
    for i in range(0,blue_bottom*2+1):
        draw.line([(0, background.height-i), (background.width, background.height-i)], tuple(t_co), width=1)

    for i in range(0, 50):
        star_color = (random.randint(215, 255), random.randint(215, 255), random.randint(215, 255))
        draw.point((random.randint(0, background.width), int(random.triangular(0, 300, 20))), fill=star_color)

    for i in range(0, 15):
        star_color = (random.randint(215, 255), random.randint(215, 255), random.randint(215, 255))
        star_location = array([random.randint(0, background.width), int(random.triangular(0, 300, 20))])
        star_size = random.randint(2, 3)
        angle = random.random()*math.pi
        leg_count = 2
        line_width = random.randint(1, 2)
        for j in range(0, leg_count):
            start_point = array([math.sin(angle), math.cos(angle)])*star_size
            end_point = array([-math.sin(angle), -math.cos(angle)])*star_size
            draw.line((tuple(star_location+start_point), tuple(star_location+end_point)), fill=star_color, width=line_width, joint=None)
            angle += math.pi/leg_count

    background.paste(globe, (0, 0), globe)

    # paint launching rocket

    rocket1 = Image.open("launch"+str(random.randint(0,5))+".png")
    rocket1 = rocket1.convert('RGBA')
    rocket1 = randomize_colors(rocket1)

    rocket_side = random.randint(0, 1)
    if rocket_side == 0:
        rocket1 = rocket1.rotate(-15, resample=Image.BICUBIC, expand=True)
        background.paste(rocket1, (background.width - rocket1.width, background.height-rocket1.height), rocket1)
    else:
        rocket1 = rocket1.rotate(15, resample=Image.BICUBIC, expand=True)
        background.paste(rocket1, (0, background.height-rocket1.height), rocket1)

    # paint moon

    background.paste(moon, ((0, background.width-300)[rocket_side], -130), moon)

    # finally, add bitcoin LN boltcard logo

    background.paste(bitcoin_logo_text, (0, 0), bitcoin_logo_text)

    background.show()

    # generate back side, first the sky

    f_co = (24, 32, 32)
    t_co = (135*0.3, 206*0.3, 235*0.3)
    for i, color in enumerate(interpolate(f_co, t_co, background.height)):
        draw.line([(0, i), (background.width, i)], tuple(color), width=1)

    for i in range(0, 100):
        star_color = (random.randint(215, 255), random.randint(215, 255), random.randint(215, 255))
        draw.point((random.randint(0, background.width), int(random.triangular(0, background.height, background.height/2))), fill=star_color)

    for i in range(0, 30):
        star_color = (random.randint(215, 255), random.randint(215, 255), random.randint(215, 255))
        star_location = array([random.randint(0, background.width), int(random.triangular(0, background.height, background.height/2))])
        star_size = random.randint(2, 3)
        angle = random.random()*math.pi
        leg_count = 2
        line_width = random.randint(1, 2)
        for j in range(0, leg_count):
            start_point = array([math.sin(angle), math.cos(angle)])*star_size
            end_point = array([-math.sin(angle), -math.cos(angle)])*star_size
            draw.line((tuple(star_location+start_point), tuple(star_location+end_point)), fill=star_color, width=line_width, joint=None)
            angle += math.pi/leg_count

    moon_background = Image.open("moon_background.png")
    moon_background = moon_background.convert('RGBA')
    moon_background = randomize_colors(moon_background)
    background.paste(moon_background, (0, 0), moon_background)

    astronaut = Image.open("astronaut"+str(random.randint(0,5))+".png")

    astronaut_side = random.randint(0, 1)
    if astronaut_side == 0:
        astronaut = astronaut.rotate(-15, resample=Image.BICUBIC, expand=True)
        background.paste(astronaut, (background.width - astronaut.width-30, background.height-astronaut.height-30), astronaut)
    else:
        astronaut = astronaut.rotate(15, resample=Image.BICUBIC, expand=True)
        background.paste(astronaut, (30, background.height-astronaut.height-30), astronaut)

    rover = Image.open("rover"+str(random.randint(0,1))+".png")
    if astronaut_side == 1:
        rover = rover.rotate(-15, resample=Image.BICUBIC, expand=True)
        background.paste(rover, (background.width - rover.width-30, background.height-rover.height-30), rover)
    else:
        rover = rover.rotate(15, resample=Image.BICUBIC, expand=True)
        background.paste(rover, (30, background.height-rover.height-30), rover)

    import qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=0,
    )
    qr.add_data(LNPAY_URL)
    qr.make(fit=True)

    lnpay_qr = qr.make_image(fill_color="black", back_color="white")

    background.paste(lnpay_qr, (30, 30), lnpay_qr)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=0,
    )
    qr.add_data(BALANCE_URL)
    qr.make(fit=True)

    lnpay_qr = qr.make_image(fill_color="black", back_color="white")

    background.paste(lnpay_qr, (background.width-lnpay_qr.size[0]-30, 30), lnpay_qr)

    font = ImageFont.truetype("Ubuntu-Medium.ttf", size=24)
    draw.text((30+lnpay_qr.size[0]/2, 35+lnpay_qr.size[0]), f"LNPay url", font=font, anchor="mt",)
    draw.text((background.width-lnpay_qr.size[0]/2-30, 35+lnpay_qr.size[0]), f"Balance", font=font, anchor="mt",)

    draw.text((background.width/2, 30), f"btcmap.org/map?nfc", font=font, anchor="mt",)
    # draw.text((background.width/2, 60), f"boltcard.org", font=font, anchor="mt",)

    draw.text((background.width/2, background.height), f"boltcard.org", font=font, anchor="mt",)

    background.show()

for i in range(0, 5):
    random.seed()
    create_card_graphics()


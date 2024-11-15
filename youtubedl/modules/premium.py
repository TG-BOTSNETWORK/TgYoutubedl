import pyrogram
from pyrogram import Client, filters
import qrcode
import requests
from io import BytesIO
from phonepe import PhonePe


# Replace with your PhonePe Merchant ID, Merchant Password, and API Key
merchant_id = "your_merchant_id"
merchant_password = "your_merchant_password"
api_key = "your_api_key"

@app.on_message(filters.command("premium"))
async def premium_command(client, message):
    text = "**Premium Benefits:**\n\n* Benefit 1\n* Benefit 2\n* Benefit 3\n\n**Choose a Plan:**"
    keyboard = [
        [
            pyrogram.InlineKeyboardButton("50₹ - 10 Days", callback_data="plan_50"),
            pyrogram.InlineKeyboardButton("100₹ - 30 Days", callback_data="plan_100"),
            pyrogram.InlineKeyboardButton("150₹ - 45 Days", callback_data="plan_150")
        ]
    ]
    await message.reply_text(text, reply_markup=pyrogram.InlineKeyboardMarkup(keyboard))

@app.on_callback_query(filters.regex("^plan_"))
async def handle_plan_selection(client, query):
    plan = query.data.split("_")[1]
    amount = int(plan)
    upi_id = "mr.nobitha123@axl"

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"upi://pay?pa={upi_id}&pn=PhonePe&am={amount}")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')

    await query.message.reply_photo(img_byte_arr, caption="Scan this QR code to pay:")
    await query.message.reply_text("**Pay the amount and send the UTR number.**")

@app.on_message(filters.private & filters.text)
async def handle_utr(client, message):
    utr_number = message.text

    # Initialize PhonePe API client
    phonepe = PhonePe(merchant_id, merchant_password, api_key)

    # Verify UTR
    try:
        response = phonepe.verify_transaction(utr_number)
        if response['status'] == 'SUCCESS':
            # Download invoice
            invoice_url = response['invoiceUrl']
            response = requests.get(invoice_url)
            invoice_file = BytesIO(response.content)
            await message.reply_document(invoice_file, filename="invoice.pdf")
        else:
            await message.reply_text("Invalid UTR number. Please try again.")
    except Exception as e:
        await message.reply_text(f"Error verifying transaction: {str(e)}")

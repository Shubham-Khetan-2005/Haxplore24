import vonage

client = vonage.Client(key="95f708ee", secret="BthcRzWW3MD6QQw1")
sms = vonage.Sms(client)

responseData = sms.send_message(
    {
        "from": "Vonage APIs",
        "to": "916396882459",
        "text": "A text message sent using the Nexmo SMS API",
    }
)

if responseData["messages"][0]["status"] == "0":
    print("Message sent successfully.")
else:
    print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
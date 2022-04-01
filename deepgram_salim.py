# Code written by Salim Oyinlola
from deepgram import Deepgram
import asyncio
import aiohttp

DEEPGRAM_API_KEY = '8eedf82d6059dc77147c29c34a80b6508e6e6f3c'

URL = 'http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourlw_online_nonuk'

async def main():
  # Initialize the Deepgram SDK
  deepgram = Deepgram(DEEPGRAM_API_KEY)

  
  try:
    deepgramLive = await deepgram.transcription.live({
      'punctuate': True,
      'interim_results': False,
      'language': 'en-GB' 
    })
  except Exception as e:
    print(f'Could not open socket: {e}')
    return

  deepgramLive.registerHandler(deepgramLive.event.CLOSE, lambda c: print(f'Connection closed with code {c}.'))

  
  deepgramLive.registerHandler(deepgramLive.event.TRANSCRIPT_RECEIVED, print)
  
  
  async with aiohttp.ClientSession() as session:
    async with session.get(URL) as audio:
      while True:
        deepgramLive.send(await audio.content.readany())

  
  await deepgramLive.finish()


asyncio.run(main())


#Twitter @SalimOpines: https://twitter.com/SalimOpines
#Github: https://www.github.com/salimcodes

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import modelform_factory
from django.template import RequestContext
from os.path import exists
import os, os.path,time
import azure.cognitiveservices.speech as speechsdk
import mimetypes


#from voices.models import Voice, Region_lan

# Set up the subscription info for the Speech Service:

speech_key, service_region = "93b735df765e4018851f272733389f0e", "eastus"

def speech_synthesis_with_voice(region='en-US',person='JennyNeural', text="This is a sample"):
    #"""performs speech synthesis to the default speaker with specified voice"""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    # Sets the synthesis voice name.
    # e.g. "Microsoft Server Speech Text to Speech Voice (en-US, JennyNeural)".
    # The full list of supported voices can be found here:
    # https://aka.ms/csspeech/voicenames
    # And, you can try get_voices_async method to get all available voices (see speech_synthesis_get_available_voices() sample below).
    voice = "Microsoft Server Speech Text to Speech Voice ({}, {})".format(region,person)
    #print(voice)
    speech_config.speech_synthesis_voice_name = voice
    # Creates a speech synthesizer for the specified voice,
    # using the default speaker as audio output.
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config,audio_config=audio_config)
  # Subscribes to events
    speech_synthesizer.synthesis_started.connect(lambda evt: print("Synthesis started: {}".format(evt)))
    speech_synthesizer.synthesizing.connect(lambda evt: print("Synthesis ongoing, audio chunk received: {}".format(evt)))
    speech_synthesizer.synthesis_completed.connect(lambda evt: print("Synthesis completed: {}".format(evt)))
    
    # Receives a text from console input and synthesizes it to speaker.
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}] completed. Hooray!".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
    else: 
        print("reason is: {}".format(speech_synthesis_result.reason))

def speech_synthesis_to_mp3_file(region='en-US',person='JennyNeural', text="This is a sample"):
    """performs speech synthesis to an mp3 file"""
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Sets the synthesis output format.
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)

    # And, you can try get_voices_async method to get all available voices (see speech_synthesis_get_available_voices() sample below).
    voice = "Microsoft Server Speech Text to Speech Voice ({}, {})".format(region,person)
    speech_config.speech_synthesis_voice_name = voice
  
    # Creates a speech synthesizer using file as audio output.
    # Replace with your own audio file name.
    ts=time.time()
    file_name = "{}{}{}.mp3".format(region,person,ts)
    
    audio_number=len([mp3 for mp3 in os.listdir('mp3') if os.path.isfile(mp3)])
   # print("the total number of mp3 files in this folder is {}".format(audio_number))
    if exists(file_name) is True:
        file_name="{}{}{}{}.mp3".format(region,person,ts,audio_number)
    file_path="mp3\{}".format(file_name)
    
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)

       # Subscribes to events
    speech_synthesizer.synthesis_started.connect(lambda evt: print("Synthesis started: {}".format(evt)))
    speech_synthesizer.synthesizing.connect(lambda evt: print("Synthesis ongoing, audio chunk received: {}".format(evt)))
    speech_synthesizer.synthesis_completed.connect(lambda evt: print("Synthesis completed: {}".format(evt)))
    
    result = speech_synthesizer.speak_text_async(text).get()
    os.chmod('mp3',0o77)
        # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}], and the audio was saved to [{}]".format(text, file_name))
    elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))      
    return file_name
# Create your views here.


def welcome(request):
    text2 =''
    if request.method=="POST":
        
        #user has pressed the Preview button
        region=request.POST.get("region") #This line pass the actual region as it gets an integer for the order of the region in Voice region.
        person=request.POST.get("voice_person")
        text=request.POST.get("text")           
        print(region)
        print(person)
        print(text)
        if request.POST.get("preview")=="preview":
            speech_synthesis_with_voice(region,person, text)
            return render(request,"website/welcome.html",
            {"message": "Below are all available voices for you to choose from",
             "text": text,
             "region":region,
             "person":person,
              },
            )
        else:
            speech_synthesis_to_mp3_file(region,person,text)
            file_name=speech_synthesis_to_mp3_file(region,person, text)
            return render (request,"website/download_mp3.html",
                           {"file_name":file_name},
                           )
        
    
    else:
        return render(request,"website/welcome.html",
                  {
                   "text": text2
                   },
                  )

def download_mp3_page(request,file_name):
    
    return response

def download_mp3(request,file_name):
    fl_path = 'mp3/'+file_name
    fl = open(fl_path, 'rb')
    mime_type, _ = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % file_name
    return response



def about(request):
    return HttpResponse("This is a project created during the Fix, Hack, Learn week long event at E+D") 
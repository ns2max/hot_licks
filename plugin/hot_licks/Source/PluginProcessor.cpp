/*
 * This file contains the basic framework code for a JUCE plugin that uses the ONNX runtime for deep inference.
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

#include "onnxruntime_cxx_api.h"
#include <thread>
#include <vector>
#include <iostream>
#include <stdlib.h>
#include <unistd.h>
#include <iomanip>

float currNote = 0;
float ptcBnd = 0;
float tmpNote = 0;
const int buffer_len = 41;
const int num_labels = 3;
std::vector <float> noteBuffer;
std::vector <float> resBuffer;

juce::OSCMessage osc1("/guitar/data1");
juce::OSCMessage osc2("/guitar/data2");
juce::OSCMessage osc3("/piano/data1");
juce::OSCMessage osc4("/piano/data2");
juce::OSCMessage osc5("/drum/data1");
juce::OSCMessage osc6("/drum/data2");
juce::OSCMessage enable("/enable/data");

// #define MODEL_PATH "/home/mind/hot_licks/saturation_model_1.onnx.onnx"
// std::string filename = "/home/mind/hot_licks/saturation_model_1.onnx";

//=================================================enable=============================
OnnxTemplatePluginAudioProcessor::OnnxTemplatePluginAudioProcessor()
#ifndef JucePlugin_PreferredChannelConfigurations
     : AudioProcessor (BusesProperties()
                     #if ! JucePlugin_IsMidiEffect
                      #if ! JucePlugin_IsSynth
                       .withInput  ("Input",  juce::AudioChannelSet::stereo(), true)
                      #endif
                       .withOutput ("Output", juce::AudioChannelSet::stereo(), true)
                     #endif
                       )
#endif
{
    // interpreter = InferenceEngine::createInterpreter(MODEL_PATH, true);
    
}

OnnxTemplatePluginAudioProcessor::~OnnxTemplatePluginAudioProcessor()
{
    recThread.stopThread(10);
    onnxInference.stopThread(10);
}

//==============================================================================
const juce::String OnnxTemplatePluginAudioProcessor::getName() const
{
    return JucePlugin_Name;
}

bool OnnxTemplatePluginAudioProcessor::acceptsMidi() const
{
   #if JucePlugin_WantsMidiInput
    return true;
   #else
    return false;
   #endif
}

bool OnnxTemplatePluginAudioProcessor::producesMidi() const
{
   #if JucePlugin_ProducesMidiOutput
    return true;
   #else
    return false;
   #endif
}

bool OnnxTemplatePluginAudioProcessor::isMidiEffect() const
{
   #if JucePlugin_IsMidiEffect
    return true;
   #else
    return false;
   #endif
}

double OnnxTemplatePluginAudioProcessor::getTailLengthSeconds() const
{
    return 0.0;
}

int OnnxTemplatePluginAudioProcessor::getNumPrograms()
{
    return 1;   // NB: some hosts don't cope very well if you tell them there are 0 programs,
                // so this should be at least 1, even if you're not really implementing programs.
}

int OnnxTemplatePluginAudioProcessor::getCurrentProgram()
{
    return 0;
}

void OnnxTemplatePluginAudioProcessor::setCurrentProgram (int index)
{
}

const juce::String OnnxTemplatePluginAudioProcessor::getProgramName (int index)
{
    return {};
}

void OnnxTemplatePluginAudioProcessor::changeProgramName (int index, const juce::String& newName)
{
}

//==============================================================================
void OnnxTemplatePluginAudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    

    osc1.addInt32(1);
    osc2.addInt32(1);
    osc3.addInt32(1);
    osc4.addInt32(1);
    osc5.addInt32(1);
    enable.addInt32(1);

    recThread.startThread();
    onnxInference.startThread();

    if (onnxInference.sender.connect("MagicQ", 8000)){
        std::cout<< "OSC connected" << std::endl;

    }

    

    

}

void OnnxTemplatePluginAudioProcessor::releaseResources()
{
    // When playback stops, you can usstd::endl;e this as an opportunity to free up any
    // spare memory, etc.
}

#ifndef JucePlugin_PreferredChannelConfigurations
bool OnnxTemplatePluginAudioProcessor::isBusesLayoutSupported (const BusesLayout& layouts) const
{
  #if JucePlugin_IsMidiEffect
    juce::ignoreUnused (layouts);
    return true;
  #else
    // This is the place where you check if the layout is supported.
    // In this template code we only support mono or stereo.
    // Some plugin hosts, such as certain GarageBand versions, will only
    // load plugins that support stereo bus layouts.
    if (layouts.getMainOutputChannelSet() != juce::AudioChannelSet::mono()
     && layouts.getMainOutputChannelSet() != juce::AudioChannelSet::stereo())
        return false;

    // This checks if the input layout matches the output layout
   #if ! JucePlugin_IsSynth
    if (layouts.getMainOutputChannelSet() != layouts.getMainInputChannelSet())
        return false;
   #endif

    return true;
  #endif
}
#endif

void OnnxTemplatePluginAudioProcessor::processBlock (juce::AudioBuffer<float>& buffer, juce::MidiBuffer& midiMessages)
{

    for (auto midiMessage : midiMessages) {
        auto midiEvent = midiMessage.getMessage();
        auto note = midiEvent.getNoteNumber();
        // std::cout << note << " " << midiEvent.getDescription() << " " << midiEvent.getTimeStamp() << std::endl;

        if (midiEvent.isNoteOn()) {
            tmpNote = midiEvent.getNoteNumber();
            currNote = tmpNote + 1;
            }
        if (midiEvent.isPitchWheel()&&tmpNote!=0) {
            ptcBnd = midiEvent.getPitchWheelValue();
            currNote = tmpNote + 1 + (ptcBnd-8192)/(8192/2);
        }
        if (midiEvent.isNoteOff()) {
            tmpNote = 0;
            currNote = 1;
        }

        if (noteBuffer.size() == buffer_len)
            noteBuffer.assign(noteBuffer.begin() + 1, noteBuffer.end());
        noteBuffer.push_back(currNote); 

        break;
    }
}

//==============================================================================
bool OnnxTemplatePluginAudioProcessor::hasEditor() const
{
    return true; // (change this to false if you choose to not supply an editor)
}

juce::AudioProcessorEditor* OnnxTemplatePluginAudioProcessor::createEditor()
{
    return new OnnxTemplatePluginAudioProcessorEditor (*this);
}

//==============================================================================
void OnnxTemplatePluginAudioProcessor::getStateInformation (juce::MemoryBlock& destData)
{
    // You should use this method to store your parameters in the memory block.
    // You could do that either as raw data, or use the XML or ValueTree classes
    // as intermediaries to make it easy to save and load complex data.
}

void OnnxTemplatePluginAudioProcessor::setStateInformation (const void* data, int sizeInBytes)
{
    // You should use this method to restore your parameters from this memory block,
    // whose contents will have been created by the getStateInformation() call.
}

//==============================================================================
// This creates new instances of the plugin..
juce::AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new OnnxTemplatePluginAudioProcessor();
}



void OnnxTemplatePluginAudioProcessor::recordingThread::check_notes(){
    while (34) {
        usleep(6000);
        // std::cout << currNote << "\t\t\t" << noteBuffer.size() << std::endl;

        if (noteBuffer.size() == buffer_len)
            noteBuffer.assign(noteBuffer.begin() + 1, noteBuffer.end());
        noteBuffer.push_back(currNote); 

        if (noteBuffer.size() == buffer_len - 1)
            std::cout << "READY SET GO!!!" << std::endl;
    }
} 

void OnnxTemplatePluginAudioProcessor::inferenceThread::inference_push(){
    OnnxTemplatePluginAudioProcessor::onnxModel inference_model;
    
    std::cout << "inference thread" << std::endl;
    std::cout << inference_model.filename << std::endl;
    std::cout << "buffer: " << buffer_len << std::endl;


    Ort::TypeInfo inputTypeInfo = inference_model.session.GetInputTypeInfo(0);
    auto inputTensorInfo = inputTypeInfo.GetTensorTypeAndShapeInfo();
    std::vector<int64_t> inputDims = inputTensorInfo.GetShape();
    for (int i=0; i< inputDims.size(); i++)
        std::cout << i << " " << inputDims[i] << std::endl;
    std::cout <<std::endl;

    Ort::TypeInfo outputTypeInfo = inference_model.session.GetOutputTypeInfo(0);
    auto outputTensorInfo = outputTypeInfo.GetTensorTypeAndShapeInfo();
    ONNXTensorElementDataType outputType = outputTensorInfo.GetElementType();
    std::vector<int64_t> outputDims = outputTensorInfo.GetShape();
    for (int i=0; i< outputDims.size(); i++)
        std::cout << i << " " << outputDims[i] << std::endl;
    std::cout <<std::endl;

    sender.sendToIPAddress("192.168.0.100", 7700, enable);



    std::vector<float> inputfill;
    for (int p=0; p<buffer_len; p++)
        inputfill.push_back(1.0);




    std::array<float, 3> results; 
    int lightDelay = 5000000;
    while (34) {
        usleep(50000);
        if (noteBuffer.size() == buffer_len) { 
            results = inference_model.inference(noteBuffer);
            // std::cout << currNote << "\t|\t" << results[0] << " \t" << results[1] << " \t" << results[2] << std::endl;


            for(int p=0; p<3; p++)
                std::cout << std::fixed << std::setprecision(4) << results[p] << "\t|\t";
            std::cout << std::endl;
 
            // if(results[1] > 9){
            //     std::cout << "-----------------------------------------------------------PAT 1-----" << std::endl;
            //     sender.sendToIPAddress("192.168.0.100", 7700, osc5);
            //     usleep(lightDelay);
            // }


            if(results[2] > 1.9){
                std::cout << "-----------------------------------------------------------PAT 2-----" << std::endl;
                sender.sendToIPAddress("192.168.0.150", 7700, osc1);
                copy(inputfill.begin(), inputfill.end(), noteBuffer.begin());
                usleep(lightDelay);
            }

            // if(results[3] > 9){
            //     std::cout << "------------------------------------------------------------PAT 3----" << std::endl;
            //     sender.sendToIPAddress("192.168.0.101", 7700, osc3);
            //     copy(inputfill.begin(), inputfill.end(), noteBuffer.begin());
            //     usleep(lightDelay);
            // }

            // if(results[4] > 8){
            //     std::cout << "------------------------------------------------------------PAT 4----" << std::endl;
            //     sender.sendToIPAddress("192.168.0.100", 7700, osc4);
            //     copy(inputfill.begin(), inputfill.end(), noteBuffer.begin());
            //     usleep(lightDelay);
            // }

            // if(results[5] > 9){
            //     std::cout << "------------------------------------------------------------PAT 5----" << std::endl;
            //     sender.sendToIPAddress("192.168.0.100", 7700, osc5);
            //     copy(inputfill.begin(), inputfill.end(), noteBuffer.begin());
            //     usleep(lightDelay);
            // }
        }
    }
}



std::array<float, 3> OnnxTemplatePluginAudioProcessor::onnxModel::inference(const std::vector<float> inputVec){
    const std::array<int64_t, 3> inputShape = { 1,buffer_len, 1 };
    const std::array<int64_t, 2> outputShape = { 1,3 };

    std::array<float, buffer_len> input;
    std::array<float, num_labels> results;

    copy(inputVec.begin(), inputVec.end(), input.begin());

    auto memory_info = Ort::MemoryInfo::CreateCpu(OrtDeviceAllocator, OrtMemTypeCPU);
    auto inputTensor = Ort::Value::CreateTensor<float>(memory_info, input.data(), input.size(), inputShape.data(), inputShape.size());
    auto outputTensor = Ort::Value::CreateTensor<float>(memory_info, results.data(), results.size(), outputShape.data(), outputShape.size());

    Ort::AllocatorWithDefaultOptions ort_alloc;
    const char *inputName = session.GetInputName(0, ort_alloc);
    const char *outputName = session.GetOutputName(0, ort_alloc);

    std::vector<const char *> inputNames;
    std::vector<const char *> outputNames;

    inputNames.push_back(inputName);
    outputNames.push_back(outputName);


    session.Run(Ort::RunOptions{nullptr}, inputNames.data(), &inputTensor, 1, outputNames.data(), &outputTensor, 1);

    return results;
}
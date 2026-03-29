/*
 * This file contains the basic framework code for a JUCE plugin that uses the ONNX runtime for deep inference.
*/

#pragma once

#include <JuceHeader.h>

#include "onnxwrapper.h" // Put your ONNX code here
#include "onnxruntime_cxx_api.h"


//==============================================================================
/**
*/
class OnnxTemplatePluginAudioProcessor  : public juce::AudioProcessor
{
public:
    //==============================================================================
    OnnxTemplatePluginAudioProcessor();
    ~OnnxTemplatePluginAudioProcessor() override;

    //==============================================================================
    void prepareToPlay (double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;

   #ifndef JucePlugin_PreferredChannelConfigurations
    bool isBusesLayoutSupported (const BusesLayout& layouts) const override;
   #endif

    void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    //==============================================================================
    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    //==============================================================================
    const juce::String getName() const override;

    bool acceptsMidi() const override;
    bool producesMidi() const override;
    bool isMidiEffect() const override;
    double getTailLengthSeconds() const override;

    //==============================================================================
    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram (int index) override;
    const juce::String getProgramName (int index) override;
    void changeProgramName (int index, const juce::String& newName) override;

    //==============================================================================
    void getStateInformation (juce::MemoryBlock& destData) override;
    void setStateInformation (const void* data, int sizeInBytes) override;

    class onnxModel{
        public:
            Ort::Env env;  //()ORT_LOGGING_LEVEL_WARNING, "onnx-test");
            Ort::SessionOptions session_options;
            // session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
            // session_options.SetOptimizedModelFilePath("optimized_model.onnx.tmp");
            // std::string filename = "/home/mind/hot_licks/model.onnx";
            std::string filename = "/home/mind/hot_licks/guitar.onnx";
            // std::string filename = "/home/mind/hot_licks/test5.onnx";
            Ort::Session session = Ort::Session(env, filename.c_str(), session_options);

            std::array<float, 3> inference(const std::vector<float> inputVec);
    };
    int patFound = 0;

private:
    //==============================================================================
    class recordingThread : public juce::Thread{
        public:
        recordingThread() : juce::Thread("background recording thread"){
        }
        void run() override{
            check_notes();
        }
        void check_notes();
    };
    recordingThread recThread;

    class inferenceThread : public juce::Thread{
        public:
        inferenceThread() : juce::Thread("background inference thread"){
        }
        void run() override{
            inference_push();
        }
        void inference_push();
        juce::OSCSender sender;
    };
    inferenceThread onnxInference;
    


    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (OnnxTemplatePluginAudioProcessor)
};

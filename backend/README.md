
1. The patterns should be .mid files and inside directory _midi_in_ 
2. Each musician has a unique ID which is represented by _art_id_ in the code. 
3. Consider the example _art_id = 52_, then each pattern should be named _52_0_0.mid_, _52_1_0.mid_, _52_2_0.mid_, ...
4. _create_data.py_ will read the data, create the synthetic variations, and dump a csv file in _data/_ 
5. _sample_data.py_ will sample the data that was previously created, and dump the files in _sampled_data/_ 
6. Finally _rnn_test_v3.py_ will read the sampled files, train and save the model
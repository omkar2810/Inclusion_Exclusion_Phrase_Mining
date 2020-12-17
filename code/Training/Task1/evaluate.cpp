#include<bits/stdc++.h>

using namespace std;

struct Res
{
    vector<double> vec[3];  
};

Res testSequential(vector<vector<string> > &sents, 
                                         vector<vector<string> > &labels) {
  uint nExprPredicted = 0;
  double nExprPredictedCorrectly = 0;
  uint nExprTrue = 0;
  double precNumerProp = 0, precNumerBin = 0;
  double recallNumerProp = 0, recallNumerBin = 0;
  for (uint i=0; i<sents.size(); i++) { // per sentence
    vector<string> labelsPredicted;
    // forward(sents[i]);

    for (uint j=0; j<sents[i].size(); j++) {
        labelsPredicted.push_back(sents[i][j]);
    }
    // assert(labelsPredicted.size() == y.cols());


    string y, t, py="", pt="";
    uint match = 0;
    uint exprSize = 0;
    vector<pair<uint,uint> > pred, tru;
    int l1=-1, l2=-1;

    if (labels[i].size() != labelsPredicted.size())
      cout << labels[i].size() << " " << labelsPredicted.size() << endl;
    for (uint j=0; j<labels[i].size(); j++) { // per token in a sentence
      t = labels[i][j];
      y = labelsPredicted[j];

      if (t == "B") {
        //nExprTrue++;
        if (l1 != -1)
          tru.push_back(make_pair(l1,j));
        l1 = j;
      } else if (t == "I") {
        // cout<<"Sentence: "<<i<<" Index: "<<j<<endl;
        ;
        // assert(l1 != -1);
      } else if (t == "O") {
        if (l1 != -1)
          tru.push_back(make_pair(l1,j));
        l1 = -1;
      } else{
          cout<<t<<endl;
        assert(false);
      }
      if ((y == "B") || ((y == "I") && ((py == "") || (py == "O")))) {
        nExprPredicted++;
        if (l2 != -1)
          pred.push_back(make_pair(l2,j));
        l2 = j;
      } else if (y == "I") {
        assert(l2 != -1);
      } else if (y == "O") {
        if (l2 != -1)
          pred.push_back(make_pair(l2,j));
        l2 = -1;
      } else { 
        cout << y << endl;
        assert(false);
      }

      py = y;
      pt = t;
    }
    if ((l1 != -1) && (l1 != labels[i].size()))
      tru.push_back(make_pair(l1,labels[i].size()));
    if ((l2 != -1) && (l2 != labels[i].size()))
      pred.push_back(make_pair(l2,labels[i].size()));

    vector<bool> trum = vector<bool>(tru.size(),false);
      vector<bool> predm = vector<bool>(pred.size(),false);
    for (uint a=0; a<tru.size(); a++) {
      pair<uint,uint> truSpan = tru[a];
      nExprTrue++;
      for (uint b=0; b<pred.size(); b++) {
        pair<uint,uint> predSpan = pred[b];

        uint lmax, rmin;
        if (truSpan.first > predSpan.first)
          lmax = truSpan.first;
        else
          lmax = predSpan.first;
        if (truSpan.second < predSpan.second)
          rmin = truSpan.second;
        else
          rmin = predSpan.second;

        uint overlap = 0;
        if (rmin > lmax)
          overlap = rmin-lmax;
        if (predSpan.second == predSpan.first) cout << predSpan.first << endl;
        assert(predSpan.second != predSpan.first);
        precNumerProp += (double)overlap/(predSpan.second-predSpan.first);
        recallNumerProp += (double)overlap/(truSpan.second-truSpan.first);
        if (!predm[b] && overlap > 0) {
          precNumerBin += (double)(overlap>0);
          predm[b] = true;
        }
        if (!trum[a] && overlap>0) {
          recallNumerBin += 1;
          trum[a]=true;
        }
      }
    }

  }
  double precisionProp = (nExprPredicted==0) ? 1 : precNumerProp/nExprPredicted;
  double recallProp = recallNumerProp/nExprTrue;
  double f1Prop = (2*precisionProp*recallProp)/(precisionProp+recallProp);
  double precisionBin = (nExprPredicted==0) ? 1 : precNumerBin/nExprPredicted;
  double recallBin = recallNumerBin/nExprTrue;
  double f1Bin = (2*precisionBin*recallBin)/(precisionBin+recallBin);

  Res results;
  results.vec[0].push_back(precisionProp); results.vec[0].push_back(precisionBin);
  results.vec[1].push_back(recallProp); results.vec[1].push_back(recallBin);
  results.vec[2].push_back(f1Prop); results.vec[2].push_back(f1Bin);
  return results;
}


int main()
{
    vector<vector<string> > pred;
    vector<vector<string> > labels;

    std::ifstream file("labels.txt");
    if (file.is_open()) {
        std::string line;
        while (std::getline(file, line)) 
        {
            // using printf() in all tests for consistency
            vector<string> temp;
            for(int i=0;i<line.length();i+=2)
            {
                string tag(1,line[i]);
                temp.push_back(tag);
            }
            pred.push_back(temp);
        }
        file.close();
    }


    std::ifstream file1("pred.txt");
    if (file1.is_open()) {
        std::string line;
        while (std::getline(file1, line)) 
        {
            // using printf() in all tests for consistency
            vector<string> temp;
            for(int i=0;i<line.length();i+=2)
            {
                string tag(1,line[i]);
                temp.push_back(tag);
            }
            labels.push_back(temp);
        }
        file1.close();
    }

    // for(int i=0;i<pred.size();i++)
    // {
    //     for(int j=0;j<pred[i].size();j++)
    //         cout<<pred[i][j];
    //     cout<<endl;
    // }
    // for(int i=0;i<labels.size();i++)
    // {
    //     for(int j=0;j<labels[i].size();j++)
    //         cout<<labels[i][j];
    //     cout<<endl;
    // }

    Res result = testSequential(pred,labels);

    cout<<result.vec[0][0]<<" "<<result.vec[0][1]<<endl;
    cout<<result.vec[1][0]<<" "<<result.vec[1][1]<<endl;
    cout<<result.vec[2][0]<<" "<<result.vec[2][1]<<endl;
    return 0;
}
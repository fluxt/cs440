#include <string>
#include <iostream>

using namespace std;

int main() {
  string line;
  int height = 0;
  while (getline(cin, line)) {
    if (line.back() == '\0') {
      line.pop_back();
    }
    cout << (int)line.back() << endl;
    cout << line.size() << endl;  
    cout << line << endl;
    height++;
  }
  cout << "i=" << height << endl;
  return 0;
}
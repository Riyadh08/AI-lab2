#include <bits/stdc++.h>
using namespace std;

class Node{
    public:
    int val;
    vector<Node*> childen;

    Node(int val, vector<Node*> childs = {}){
        this->val = val;
        childen = childs;

    }
};

int minimax(Node* node, int depth, bool maximizingPlayer){
    // Base case: leaf node or depth exhausted
    if (depth == 0 || node->childen.empty()) {
        return node->val;
    }    

    if(maximizingPlayer){
        int maxEval = INT_MIN;
        for(Node* child : node->childen){
            int eval = minimax(child, depth-1, false);
            maxEval = max(maxEval, eval);
        }
        return maxEval;
    }else{
        int minEval = INT_MAX;
        for(Node* child : node->childen){
            int eval = minimax(child, depth-1, true);
            minEval = min(minEval, eval);
        }
        return minEval;
    }
}


int main() {
    // Leaf nodes
    Node* d1 = new Node(-1);
    Node* d2 = new Node(8);
    Node* e1 = new Node(-3);
    Node* e2 = new Node(-1);
    Node* f1 = new Node(2);
    Node* f2 = new Node(1);
    Node* g1 = new Node(-3);
    Node* g2 = new Node(4);

    // Level 2
    Node* D = new Node(0, {d1, d2});
    Node* E = new Node(0, {e1, e2});
    Node* F = new Node(0, {f1, f2});
    Node* G = new Node(0, {g1, g2});

    // Level 1
    Node* B = new Node(0, {D, E});
    Node* C = new Node(0, {F, G});

    // Root
    Node* A = new Node(0, {B, C});

    int optimalValue = minimax(A, 3, true);
    cout << "Optimal value at root (A): " << optimalValue << endl;
    
    return 0;
}
/**
A full sub-graphs generation program
  and testing automation wrapper
  (selective SAT / UNSAT input graphs)
  for IITD/AI/COL333-671/2018/A3
  Version : 1.1 (2018-09-26)
          By Sachin (CSE PhD)
*/

#include <iostream>
#include <fstream>
#include <vector>
#include <string.h>
#include <unistd.h>
#include <termios.h>
#include <algorithm>

#define NN 3
#define KK 2

#define EXTN1         ".graph"
#define EXTN2         ".subgraphs"

#define R(x) ((x)?rand()%(x):0)

using namespace std;

int N,E,K;

char getch() {
        char buf = 0;
        struct termios old = {0};
        if (tcgetattr(0, &old) < 0)
                perror("tcsetattr()");
        old.c_lflag &= ~ICANON;
        old.c_lflag &= ~ECHO;
        old.c_cc[VMIN] = 1;
        old.c_cc[VTIME] = 0;
        if (tcsetattr(0, TCSANOW, &old) < 0)
                perror("tcsetattr ICANON");
        if (read(0, &buf, 1) < 0)
                perror ("read()");
        old.c_lflag |= ICANON;
        old.c_lflag |= ECHO;
        if (tcsetattr(0, TCSADRAIN, &old) < 0)
                perror ("tcsetattr ~ICANON");
        return (buf);
}

string name, script;
int unsatisfy = false, verbose = false, quiet = false;
bool parse(int argc, char* argv[])
{
    bool usage = false;
    for(int i=1 ; i<argc ; ++i)
    {
        if(argv[i][0] != '-' || argv[i][2]!='=')
        {
            usage = true;
            break;
        }
        switch(argv[i][1])
        {
            case 'f':
            case 'F':
                name = argv[i]+3;
            break;

            case 's':
            case 'S':
                script = argv[i]+3;
                if(script.length() && script[0]!='.' && script[0]!='/')
                    script.insert(0,"./");
            break;

            case 'N':
            case 'n':
                N = atoi(argv[i]+3);
                if(N < NN)
                    usage = true;
            break;

            case 'K':
            case 'k':
                K = atoi(argv[i]+3);
                if(K < KK)
                    usage = true;
            break;

            case 'U':
            case 'u':
                unsatisfy = atoi(argv[i]+3);
                if(unsatisfy)
                    unsatisfy = 1;
            break;

            case 'V':
            case 'v':
                verbose = atoi(argv[i]+3);
                if(verbose)
                    verbose = 1;
            break;

            case 'Q':
            case 'q':
                quiet = atoi(argv[i]+3);
                if(quiet)
                    quiet = 1;
            break;
        }
    }
    if(!name.size() || !N || !K)
        usage = true;
    if(N<=K)
    {
        cout << "N should be greater than K.\n"; 
        usage = true;
    }
    if(usage)
    {
        cout << "Correct Usage ->\n";
        cout << argv[0] << " -F=BaseName -N=NumNodes -K=NumSubGraphs [-S=ShellScript] [-U=UNSAT] [-V=Verbose] [-Q=QuietlyQuit]\n";
        cout << "Please give base filename without .graph extn\n";
        cout << "N >= " << NN << " and K >= " << KK << " and N > K" << endl;
        cout << "Giving a shell script to perform TAs task will automate testing.\n";
        cout << "If no script is given, user can perform tasks separately and verify.\n";
        cout << "Giving -U=1 (non-zero) enables UNSAT graph, default SAT.\n";
        cout << "Giving -V=1 (non-zero) enables verbose mode, giving some generated graph info.\n";
        cout << "Giving -Q=1 (non-zero) enables quiet mode, to exit if shell script is not given.\n";
        cout << endl;
        return 1;
    }
    return 0;
}

int main(int argc, char* argv[])
{
    cout << "\n-----------------------------------------\n";
    cout << "----- yAI Mausam ka jaadu hai mitwa -----\n";
    cout << "-----------------------------------------\n\n";
    cout << "A full sub-graphs generation program\n";
    cout << "  and testing automation wrapper\n";
    cout << "  (selective SAT / UNSAT input graphs)\n";
    cout << "  for IITD/AI/COL333-671/2018/A3\n";
    cout << "  Version : 1.1 (2018-09-26)\n";
    cout << "          By Sachin (CSE PhD)\n\n";

    cout << "Disclaimer:\n";
    cout << "  This is a student (non-TA) program.\n";
    cout << "  Please use at your own responsibility.\n";
    cout << "  Report bugs on piazza or mail me.\n\n";

    if(parse(argc, argv))
        return 1;

    cout << "Working to " << (script.length() ? "test" : "generate" ) << (unsatisfy ? " UNSAT " : " SAT ") << "graph for "
        << N << " nodes and " << K << " subgraphs." << endl;
    
    string file1 = string(name)+EXTN1;
    string file2 = string(name)+EXTN2;

    srand(time(NULL));

    ofstream outfile;
    outfile.open(file1);

    // Divide N into K parts
    vector<int> parts;
    int mode=1;
    if(K==2)
    {
        cout << "Performing node splitting.\n";
        int p = R(N-1)+1;
        parts.push_back(p);
        parts.push_back(N-p);
    }
    else if(mode==1)
    {
        cout << "Performing with hard constraints.\n";

        parts.push_back(N-3);
        while(parts.size() < K-2)
        {
            int i;
            for(i=0 ; i<parts.size() ; ++i)
                if(parts[i]>=6)
                    break;
            if(i>=parts.size())
            {
                cout << "Switching to relaxed constraints.\n";
                goto MODE_2;
            }

            int t = R(4);
            int w = R(parts.size());
            if(!t)
            {
                // Divide the max one
                int max = parts[0];
                w = 0;
                for(int i=1 ; i<parts.size() ; ++i)
                    if(parts[i]>parts[w])
                        w = i;
            }
            if(parts[w]<6)
                continue;
            int p = R(parts[w]-6)+3;
            parts[w] -= p;
            parts.push_back(p);
        }
        parts.push_back(2);
        parts.push_back(1);
    }
    else
    {
MODE_2:
        parts[R(parts.size())] += 3;
        while(parts.size() < K)
        {
            int i;
            for(i=0 ; i<parts.size() ; ++i)
                if(parts[i]>=2)
                    break;
            if(i>=parts.size())
            {
ERROR:
                cout << "This program cannot formulate a graph with given constraints.\n";
                cout << "Please choose either options -\n";
                cout << "(1) Try again with bigger N\n";
                cout << "(2) Try again with smaller K\n";
                cout << "(3) Try with some other program\n";
                outfile.close();
                return 1;
            }

            int w = R(parts.size());
            if(parts[w]<2)
                continue;
            int p = R(parts[w]-1)+1;
            parts[w] -= p;
            parts.push_back(p);
        }
    }
    // make sure first one is not 1
    if(parts[0]==1)
    {
        int i=1;
        for( ; i<parts.size() ; ++i)
        {
            if(parts[i]>1)
            {
                parts[0]++;
                parts[i]--;
                break;
            }
        }
        if(i >= parts.size())
            goto ERROR;
    }
#if 0
    cout << "Splitting into groups of : ";
    for(int i=0 ; i<parts.size() ; ++i)
        cout << parts[i] << " ";
    cout << endl;
#endif
    vector< vector<int> > G;
    G.resize(N+1);
    for(int i=0 ; i<=N ; ++i)
        G[i].resize(N+1);
    vector <pair<int,int>> range;

    cout << "Generating " << K << " subgraphs of " << N << " nodes " << (verbose ? "ranging : " : "");
    for(int p=0, done=0  ; p<parts.size() ; ++p)
    {
        int start = done+1;
        if(p)
        {
            int sz = (parts[p-1]+1)/2;
            int cnt1 = R(sz), cnt2 = R(sz);
            if(cnt1 > cnt2)
                cnt1 = cnt2;
            start -= 1 + cnt1;
        }
        int end = done + parts[p];
        for(int i=start ; i<=end ; ++i)
        {
            for(int j=start ; j<=end ; ++j)
                G[i][j] = G[j][i] = 1;
        }
        done += parts[p];
        range.push_back(make_pair(start,end));
        if(verbose)
            cout << "(" << start << "," << end << ") ";
    }
    cout << endl << endl;

    if(unsatisfy)
    {
        if(verbose)
           cout << "Removing edges for unsatisfiability.\n";
        bool dn=false;
        for(int k=0, cmp=1 ; k<K && cmp<=4 ; ++k)
        {
            if((range[k].second - range[k].first) > cmp)
            {
                G[range[k].second][range[k].first] = G[range[k].first][range[k].second] = 0;
                cmp += 3;
                dn = true;
            }
        }
        if(dn == false)
            goto ERROR;
    }

    E = 0;
    for(int i=1 ; i<=N ; ++i)
        for(int j=i+1 ; j<=N ; ++j)
            if(G[i][j])
                E++;
    outfile << N << " " << E << " " << K << endl;
    for(int i=1 ; i<=N ; ++i)
        for(int j=i+1 ; j<=N ; ++j)
            if(G[i][j])
                outfile << i << " " << j << endl;
    outfile.close();

    cout << file1 << " generated with " << N << " nodes and " << E << " edges.\n";

    if(script.length())
    {
        cout << "Executing script : " << script << " " << name << endl;
        system((script + string(" ") + name).c_str());
    }
    else if(quiet)
    {
        return 1;
    }
    else
    {
        cout << "No test script specified. Switching to interactive mode.\n";
        cout << "Pls test as directed by TA.\n";
        cout << "Press q to quit and validate the subgraphs separately.\n";
        cout << "Press Enter after generating subgraph file for validation.\n";
        int ch;
        do{
            ch = getch();
            if(ch=='q' || ch=='Q')
                return 1;
        }while(ch != 10);
    }

    cout << endl << argv[0] << " Verifying " << file2 << endl;
    ifstream infile;
    infile.open(file2);

    vector<int> done;
    done.resize(K);
    
    for(int k=0 ; k<K ; ++k)
    {
        char ch;
        int idx, cnt;
        infile >> ch;
        if(k==0 && ch=='0')
        {
            cout << "Unsatisfied result. ";
            if(unsatisfy)
               cout << "Output is correct.\n";
            else
               cout << "Output is wrong.\n";
            return 1;
        }
        if(ch!='#')
        {
            cout << "Wrong output format. Exiting.\n";
            return 1;
        }
        if(unsatisfy)
        {
            cout << "Expected unsatisfied result, but it did not come.\n";
            cout << "Stopping. Pls verify with other means.\n";
            return 1;
        }
        infile >> idx >> cnt;
        //cout << idx << " " << cnt << endl;

        if(idx != k+1)
        {
            cout << "Wrong #" << idx << ", Expected was #" << k+1 << endl;
            return 1;
        }
        if(cnt<2)
        {
            cout << "Wrong size of subgraph #"<< idx << " = " << cnt << endl;
            return 1;
        }

        vector<int> v;
        for(int i=0 ; i<cnt ; ++i)
        {
            int a;
            infile >> a;
            v.push_back(a);
        }
        sort(v.begin(), v.end());
        for(int i=1 ; i<cnt ; ++i)
        {
            if(v[i] != v[i-1]+1)
            {
                cout << "Wrong output detected for #" << idx << endl;
                cout << "Missing node " << v[i-1]+1 << endl;
                cout << "Please re-verify with other means\n";
                return 1;
            }
        }
        int i=0;
        for( ; i<K ; ++i)
        {
            if(done[i]==false && range[i].first==v[0] && range[i].second==v[cnt-1])
            {
                done[i] = true;
                break;
            }
        }
        if(i>=K)
        {
            cout << "Wrong output at #" << idx << endl;
            cout << "No subgraph found for (" << v[0] << "," << v[cnt-1] << ")\n";
            return 1;
        }
    }
    infile.close();

    for(int i=0 ; i<K ; ++i)
    {
        if(done[i]==false)
        {
            cout << "Wrong output. Missing the subgraph for (" << range[i].first << "," << range[i].second << endl;
            return 1;
        }
    }
    cout << "\nOutput is OK. All validations passed.\n\n";

    return 0;
}

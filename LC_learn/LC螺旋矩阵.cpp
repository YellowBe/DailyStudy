class Solution {
public:
    vector<vector<int>> generateMatrix(int n) {
        vector<vector<int>> res(n, vector<int>(n, 0)); // 使用vector定义一个二维数组
        int startx = 0, starty = 0; 
        int loop = n / 2;
        int mid = n / 2;
        int count = 1;
        int offset = 1;
        int i,j;
        while (loop --) {
            i = startx;
            j = starty;

            for (j = starty; j < n - offset; j++) {
                res[startx][j] = count++;
            }

            for (i = startx; i < n - offset; i++) {
                res[i][j] = count++;
            }
            for (; j>starty; j--){
                res[i][j] = count++;
            }

            //
            startx++;
            starty++;

            //
            offset += 1;
        }

        if (n % 2) {
            res[mid][mid] = count;
        }
        return res;
    }
};
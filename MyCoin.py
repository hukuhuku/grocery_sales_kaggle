C    = [3,2,1,3,0,2]
Val  = [1,5,10,50,100,500]
A    = 620


def Coin ():
    queue = []
    x = len(Val)

    for i in range(x)[::-1]:        #価値の高いコインから降りていく

        for j in range(C[i]+1)[::-1]:  #range(6)[::-1]は５→４…→0なのでC[i]を一つ大きくしないといけない
            que = []
            for k in range(j):         #それぞれのコインの数だけqueコインをつめる
                que.append(Val[i])

            if (sum(que)+sum(queue)) < A:   #<と＝で作業が似ているからまとめられそう
                for p in range(len(que)):
                    queue.append(que[p])    #queをまとてつめこもうとすると、配列として入ってしまうのでfor文で回して要素ごとに詰め込む
                break
            elif(sum(que) + sum(queue)) == A:
                for q in range(len(que)):
                    queue.append(que[q])
                res = len(queue)            #等しい時その長さを返す




    print(res)


Coin()

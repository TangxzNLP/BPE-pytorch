import pickle

class multibpe_unit(object):
    #默认从0开始合并，这个后续还要改进
    def __init__(self, path='../model/total.pkl', file_num = 2):
        self.path = path
        self.file_num = file_num
    def multibpe_unit(self):
        with open(self.path,'wb') as WF:
            sorted_store = []
            sorted_total = []
            for i in range(self.file_num):
                sorted_tokenstest = []
                strtest = '../model/model_split/splited_{}.pkl'.format(i)
                with open(strtest, 'rb') as F:
                    E = pickle.load(F)
                    sorted_tokenstest = [token for (token, freq) in E]          
                    for j in range(len(sorted_tokenstest)):
                        sorted_total.append(sorted_tokenstest[j])
            sorted_store = [(token, sorted_total.index(token)) for token in sorted_total]
            pickle.dump(sorted_store, WF)    


if __name__ == '__main__':
    a = multibpe_unit('total.pkl',2)
    a.multibpe_unit()

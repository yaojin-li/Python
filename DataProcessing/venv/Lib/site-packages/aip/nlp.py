# -*- coding: utf-8 -*-

from base import *

class AipNlp(AipBase):
    """
        Aip NLP
    """

    __wordsegUrl = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/wordseg'
    
    __wordposUrl = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/wordpos'
    
    __wordembeddingUrl = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/wordembedding'
    
    __dnnlmUrl = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/dnnlm_cn'
    
    __simnetUrl = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/simnet'
    
    __commentTagUrl = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/comment_tag'

    def _proccessResult(self, content):
        """
            formate result
        """
        
        return json.loads(content.decode('gbk', 'ignore').encode('utf8')) or {}
    
    def wordseg(self, query):
        """
            Aip wordseg
        """

        data = {}
        data['query'] = query.decode('utf8').encode('gbk', 'ignore')

        return self._request(self.__wordsegUrl, json.dumps(data, ensure_ascii=False))

    def wordpos(self, query):
        """
            Aip wordpos
        """

        data = {}
        data['query'] = query.decode('utf8').encode('gbk', 'ignore')

        return self._request(self.__wordposUrl, json.dumps(data, ensure_ascii=False))

    def wordembedding(self, query1, query2=''):
        """
            Aip wordembedding
        """

        data = {}
        data['query1'] = query1.decode('utf8').encode('gbk', 'ignore')

        if query2:
            data['query2'] = query2.decode('utf8').encode('gbk', 'ignore')
            data['tid'] = 1
        else:
            data['tid'] = 2

        return self._request(self.__wordembeddingUrl, json.dumps(data, ensure_ascii=False))

    def dnnlm(self, query):
        """
            Aip dnnlm
        """

        data = {}
        data['input_sequence'] = query.decode('utf8').encode('gbk', 'ignore')

        return self._request(self.__dnnlmUrl, json.dumps(data, ensure_ascii=False))

    def simnet(self, query1, query2, options=None):
        """
            Aip simnet
        """

        options = options or {}
        data = {}
        data['input'] = {
            'qslots':[{
                'terms_sequence': query1.decode('utf8').encode('gbk', 'ignore'),
                'type': 0,
                'items': [],
            }],
            'tslots':[{
                'terms_sequence': query2.decode('utf8').encode('gbk', 'ignore'),
                'type': 0,
                'items': [],
            }],
            'type': options.get('type', 0),
        }

        return self._request(self.__simnetUrl, json.dumps(data, ensure_ascii=False))

    def commentTag(self, comment, options=None):
        """
            Aip commentTag
        """

        options = options or {}
        data = {}
        data['comment'] = comment.decode('utf8').encode('gbk', 'ignore')
        data['type'] = str(options.get('type', '4'))
        data['entity'] = options.get('entity', 'NULL')

        return self._request(self.__commentTagUrl, json.dumps(data, ensure_ascii=False))

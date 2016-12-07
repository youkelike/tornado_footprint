import sys,math
from bisect import bisect
import hashlib
md5_constructor = hashlib.md5

class HashRing(object):
    def __init__(self,nodes):
        '''默认一个节点对应32个虚拟节点，权重可以对每个节点对应的虚拟节点数重新划分'''
        #保存环上的虚拟节点与真实节点的对应关系
        self.ring = dict()
        #保存排序后的虚拟节点
        self._sorted_keys = []
        self.total_weight = 0
        self.__generate_circle(nodes)

    def __generate_circle(self,nodes):
        for node_info in nodes:
            #没有设置权重就默认为1
            self.total_weight += node_info.get('weight',1)

        for node_info in nodes:
            weight = node_info.get('weight',1)
            node = node_info.get('host',None)
            # 当前节对应的点虚拟节点数 = 虚拟节点总数 * 当前节点的权重比例
            virtual_node_count = math.floor(32*len(nodes)*weight/self.total_weight)
            for i in range(int(virtual_node_count)):
                # 为当前节点的每个虚拟节点计算hash值
                key = self.gen_key_thirty_two('%s-%s' % (node,i))
                if key in self._sorted_keys:
                    print(key)
                    raise Exception('节点重复！')
                self.ring[key] = node
                self._sorted_keys.append(key)
        self._sorted_keys.sort()

    def get_node(self,string_key):
        pos = self.get_node_pos(string_key)
        if pos is None:
            return None
        return self.ring[self._sorted_keys[pos]].split(':')

    def get_node_pos(self,string_key):
        if not self.ring:
            return None
        key = self.gen_key_thirty_two(string_key)
        nodes = self._sorted_keys
        #获取key在有序列表nodes中的位置
        pos = bisect(nodes,key)
        return pos

    def gen_key_thirty_two(self,key):
        m = md5_constructor()
        m.update(key.encode())
        return m.hexdigest()


if __name__ == '__main__':
    nodes = [
        {'host':'127.0.0.1:80','weight':1},
        {'host':'127.0.0.1:81','weight':2},
        {'host':'127.0.0.1:82','weight':1},
    ]
    ring = HashRing(nodes)
    result = ring.get_node('79999999999999999999999')
    print(result)



# !/usr/bin/env python3
#  -*- coding: utf-8 -*-
"""
@author: Sonya
"""

import matplotlib.pyplot as plt
import requests as req  # For HTTP requests
from bs4 import BeautifulSoup  # For data scrapping
import networkx as nx  # GraphML
import argparse  # CLI

# DEFAULT settings
DEFAULT_URL = 'https://github.com/'
DEFAULT_USERNAME = 'bakirillov'
DEEP = 3
#####


def get_followers_graph(username=DEFAULT_USERNAME, deep=DEEP):
    G = nx.DiGraph()  # New Directional Graph
    parsed_users = []
    name, followers_list = parse_url(username)
    G.add_node(username)  # Zero Node
    G.nodes[username]['Name'] = name
    for x in range(0, deep-1):  # Adding followers nodes to graph
        S = nx.DiGraph(G)
        cur_nodes = S.nodes(data=True)
        for node, data in cur_nodes:
            if node in parsed_users:
                pass
            else:
                name, followers_list = parse_url(node)
                for follower in followers_list:
                    # Adding edges to sub
                    G.add_edge(follower['Username'], node)
                    # setting names
                    G.nodes[follower['Username']]['Name'] = follower['Name']
        parsed_users.append(node)
    return G


def parse_url(username=DEFAULT_USERNAME):
    resp = req.get(DEFAULT_URL+username+"?tab=followers")  # HTTP GET REQUEST
    soup = BeautifulSoup(resp.text, 'lxml')  # BS4 SOUP
    # Finding user name attribute
    name_atr = soup.find('span',
                         'p-name vcard-fullname d-block overflow-hidden')
    name = name_atr.text  # Extracting name
    followers_atr = soup.find_all('a', 'd-inline-block no-underline mb-1',
                                  href=True)
    followers_list = []
    for follower in followers_atr:
        # Extracting names of followers
        follower_name = follower.find('span', 'f4 link-gray-dark').text
        if follower_name == '':
            follower_name = 'No Name'
        else:
            pass
        # Extracting usernames of followers
        follower_username = follower['href'].lstrip('/')
        followers_list.append(dict([('Username', follower_username),
                                    ('Name', follower_name)]))
        print(follower_name + '\t' + follower_username + '\r')
    pass
    return name, followers_list


def main():
    parser = argparse.ArgumentParser(description='Github parsing script')
    parser.add_argument('--USERNAME',
                        help=f'GitHub account username \
                        (type:str, default:{DEFAULT_USERNAME})',
                        default=DEFAULT_USERNAME,
                        type=str
                        )
    parser.add_argument('--DEEP',
                        help=f'Search deep (type:int, default:{DEEP})',
                        default=DEEP,
                        type=int
                        )
    args = parser.parse_args()
    if args.USERNAME != "":
        if args.DEEP != "":
            g = get_followers_graph(args.USERNAME, args.DEEP)
        else:
            g = get_followers_graph(deep=args.DEEP)
    else:
        g = get_followers_graph()
    pos = nx.spring_layout(g)  # Drawing graph
    nx.draw_networkx_nodes(g, pos,
                           node_color='lime',
                           node_size=250,
                           alpha=0.6
                           )  # Drawing graph's nodes
    nx.draw_networkx_labels(g, pos,
                            font_size=10,
                            font_color='magenta'
                            )  # Drawing graph's labeles
    nx.draw_networkx_edges(g, pos, edgelist=g.edges,
                           arrows=True)  # Drawing arrows for edges
    nx.write_graphml(g, f'{args.USERNAME}_graph')  # Saving graph
    plt.draw()
    plt.title(f'{args.USERNAME} followers graph')
    plt.show()
    return


if __name__ == '__main__':
    main()

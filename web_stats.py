# -*- coding: utf-8 -*-
import os
from fabric.api import local


class ApacheBenchmark(object):
    def __init__(self, server_list, api_dict,
            batches_list=[20, 50, 75, 100], total=100, usr_pass=False):
        self.server_list = server_list
        self.batches_list = batches_list
        self.api_dict = api_dict
        self.total = total
        if usr_pass:
            self.usr_pass = usr_pass

        instruction_list = [
            ('"{server_name}_###.csv" using 9 smooth sbezier with lines '
                'title "{server_name}.com"'
                ).format(server_name=server_name) for server_name in
            self.server_list]
        server_instructions = ','.join(instruction_list
            ).replace('###', '{idx}')

        self.plotInstructions = ('set terminal png size 600\n'
            'set output "{key_name}_{idx}.png"\n'
            'set title "{key_name}; {total} requests, in batches of {idx}"\n'
            'set size ratio 0.6\n'
            'set grid y\n'
            'set xlabel "# requests"\n'
            'set ylabel "response time (ms)"\n'
            'plot') + server_instructions

    def run(self):
        for key_name, api in self.api_dict.iteritems():
            self.create_graphics(api, key_name)
            self.clean_up()

    def test_server(self, server, idx, api):
        local(
            ('ab -g {server}_{idx}.csv -n {total} -c {idx} '
                '{authenticate}{usr_pass} '
                'https://cabaana.{server}.com/{api}').format(
                    server=server,
                    idx=idx,
                    total=self.total,
                    api=api,
                    authenticate='-A ' if self.usr_pass else '',
                    usr_pass=self.usr_pass if self.usr_pass else ''
                )
            )

    def gnu_plot(self, idx):
        local('gnuplot plot_{idx}.p'.format(idx=idx))

    def create_graphics(self, api, key_name):
        for server in self.server_list:
            for idx in self.batches_list:
                self.test_server(server, idx, api)

        for idx in self.batches_list:
            with open('plot_{idx}.p'.format(idx=idx), 'w') as f:
                f.write(self.plotInstructions.format(
                    idx=idx,
                    total=self.total,
                    key_name=key_name,
                    ))
            self.gnu_plot(idx)

    def clean_up(self):
        path = os.path.dirname(__file__)
        for server in self.server_list:
            for idx in self.batches_list:
                file2 = os.path.join(
                    path,
                    '{server}_{idx}.csv'.format(server=server, idx=idx)
                    )
                os.remove(file2)
        for idx in self.batches_list:
            file1 = os.path.join(
                path,
                'plot_{idx}.p'.format(idx=idx)
                )
            os.remove(file1)


if __name__ == '__main__':
    ab = ApacheBenchmark(
        # this is a list of dns of the servers you want to test
        server_list=['', '', ''],
        # these are the uris you are asking on each of the servers
        api_dict={
            'landing': '',
            'company': '/api/other'
            },
        )
    ab.run()

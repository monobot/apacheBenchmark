# apacheBenchmark

**This script is a simple wrap around ++apache benchmark++, the tool allows you to test one or serveral servers using a different concurrent requests.**
**You can also authenticate your user if you need to.**

### options
- list of dns of the servers you want to test
`server_list=['', '', '']`

- the batches of requests you are sending
`batches_list=[20, 50, 75, 100]`

- the uris you are asking on each of the servers
`api_dict={'landing': '', 'company': '/api/other'}`

- the total of requests you are sending in total
`total=100`

- User:password
`usr_pass='user:password'`
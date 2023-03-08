
# 2023-02-17 16:19:59,795 [MainThread  ] [INFO ]  Retrieving http://search.maven.org/remotecontent?filepath=org/apache/tika/tika-server-standard/2.6.0/tika-server-standard-2.6.0.jar to /var/folders/ct/242_3ld56f1c5w52hw4j71w00000gn/T/tika-server.jar.
# 2023-02-17 16:38:27,466 [MainThread  ] [WARNI]  Failed to see startup log message; retrying...


from tika import parser
parsed = parser.from_file('samples/insertionSortSimple.pdf')
# print(parsed["metadata"])
print(parsed["content"])

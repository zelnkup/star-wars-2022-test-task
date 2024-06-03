# Thoughts what to improve

Using uvicorn and async django was my own initiative to play around with this solution, because I haven't had a chance to try async django yet. Additional logic expanding also was done by my own will to have complex open source project.

Initial request takes near 30 seconds, because we need to fetch all planets and store them in DB. Further requests take on average 12-13 seconds using prefetched planets.

Video [user experience](https://www.youtube.com/watch?v=uSF982kJgd0)

- Separate client and server, move to REST architecture
- Consider using light weight async frameworks(fastapi, aiohttp) for such kind of tasks
- For sake of performance, save homeworlds in cache for fast access, and refetch them from API using celery task once daily (consider if homeworlds are permanent or can change)
- Consider caching characters too and refetch them once per day/week
- Consider reusing already generated CSV for new downloads
- Consider using queue mechanism if we proceed without async django views
- Increase test coverage to 100% (add tests for views)

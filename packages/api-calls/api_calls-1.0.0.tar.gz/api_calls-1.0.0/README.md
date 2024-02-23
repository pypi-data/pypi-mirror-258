# API_CALLS

-   This package makes it easy to make api calls in python by abstracing all the logic you'd otherwise use with other packages such as requests
-   This package requires requests 2.31.0 or later versions
-   Example usage below:

    ```

    from api_calls import ApiCalls


    class CatService(ApiCalls):
        base_url = "https://cat-fact.herokuapp.com"
        timeout = 500

        def get_random_cat_fact(self):
            response = self.make_request(
                "/facts/random", method="get", params={"amount": 5})
            return (response)


    data, error = CatService().get_random_cat_fact()

    ```

To install, run:
`pip install api_calls`

# REST API Basics
## Overview
A REST API (also known as RESTful API) is an application programming interface (API or web API) that conforms to the constraints of REST architectural style and allows for interaction with RESTful web services. REST stands for representational state transfer and was created by computer scientist Roy Fielding.

<iframe width="560" height="315" src="https://www.youtube.com/embed/lsMQRaeKNDk" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## What's an API*?

An API is a set of definitions and protocols for building and integrating application software. It’s sometimes referred to as a contract between an information provider and an information user—establishing the content required from the consumer (the call) and the content required by the producer (the response). For example, the API design for a weather service could specify that the user supply a zip code and that the producer reply with a 2-part answer, the first being the high temperature, and the second being the low.  

In other words, if you want to interact with a computer or system to retrieve information or perform a function, an API helps you communicate what you want to that system so it can understand and fulfill the request. 

You can think of an API as a mediator between the users or clients and the resources or web services they want to get. It’s also a way for an organization to share resources and information while maintaining security, control, and authentication—determining who gets access to what. 

Another advantage of an API is that you don’t have to know the specifics of caching—how your resource is retrieved or where it comes from.

## REST

REST is a set of architectural constraints, not a protocol or a standard. API developers can implement REST in a variety of ways.

When a client request is made via a RESTful API, it transfers a representation of the state of the resource to the requester or endpoint. This information, or representation, is delivered in one of several formats via HTTP: JSON (Javascript Object Notation), HTML, XLT, Python, PHP, or plain text. JSON is the most generally popular file format to use because, despite its name, it’s language-agnostic, as well as readable by both humans and machines. 

Something else to keep in mind: Headers and parameters are also important in the HTTP methods of a RESTful API HTTP request, as they contain important identifier information as to the request's metadata, authorization, uniform resource identifier (URI), caching, cookies, and more. There are request headers and response headers, each with their own HTTP connection information and status codes.

In order for an API to be considered RESTful, it has to conform to these criteria:

* A client-server architecture made up of clients, servers, and resources, with requests managed through HTTP.
* [Stateless](https://www.redhat.com/en/topics/cloud-native-apps/stateful-vs-stateless) client-server communication, meaning no client information is stored between get requests and each request is separate and unconnected.
* Cacheable data that streamlines client-server interactions.
* A uniform interface between components so that information is transferred in a standard form. This requires that:
    * resources requested are identifiable and separate from the representations sent to the client.
    * resources can be manipulated by the client via the representation they receive because the representation contains enough information to do so.
    * self-descriptive messages returned to the client have enough information to describe how the client should process it.
    * hypertext/hypermedia is available, meaning that after accessing a resource the client should be able to use hyperlinks to find all other currently available actions they can take.
* A layered system that organizes each type of server (those responsible for security, load-balancing, etc.) involved the retrieval of requested information into hierarchies, invisible to the client.
* Code-on-demand (optional): the ability to send executable code from the server to the client when requested, extending client functionality. 

Though the REST API has these criteria to conform to, it is still considered easier to use than a prescribed protocol like SOAP (Simple Object Access Protocol), which has specific requirements like XML messaging, and built-in security and transaction compliance that make it slower and heavier. 

In contrast, REST is a set of guidelines that can be implemented as needed, making REST APIs faster and more lightweight, with increased scalablity—perfect for [Internet of Things (IoT)](https://www.redhat.com/en/topics/internet-of-things-120511) and [mobile app development](https://www.redhat.com/en/topics/mobile).



\* Material taken form [Redhat.com](https://www.redhat.com/en/topics/api/what-is-a-rest-api)

## Using HTTP Methods for RESTful Services
The HTTP verbs comprise a major portion of our “uniform interface” constraint and provide us the action counterpart to the noun-based resource. The primary or most-commonly-used HTTP verbs (or methods, as they are properly called) are POST, GET, PUT, PATCH, and DELETE. These correspond to create, read, update, and delete (or CRUD) operations, respectively. There are a number of other verbs, too, but are utilized less frequently. Of those less-frequent methods, OPTIONS and HEAD are used more often than others.

Below is a table summarizing recommended return values of the primary HTTP methods in combination with the resource URIs

| HTTP Verb | CRUD           | Entire Collection (e.g. /customers)                                                                  | Specific Item (e.g. /customers/{id})                                       |
| --------- | -------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| POST      | Create         | 201 (Created), 'Location' header with link to /customers/{id} containing new ID.                     | 404 (Not Found), 409 (Conflict) if resource already exists..               |
| GET       | Read           | 200 (OK), list of customers. Use pagination, sorting and filtering to navigate big lists.            | 200 (OK), single customer. 404 (Not Found), if ID not found or invalid.    |
| PUT       | Update/Replace | 405 (Method Not Allowed), unless you want to update/replace every resource in the entire collection. | 200 (OK) or 204 (No Content). 404 (Not Found), if ID not found or invalid. |
| PATCH     | Update/Modify  | 405 (Method Not Allowed), unless you want to modify the collection itself.                           | 200 (OK) or 204 (No Content). 404 (Not Found), if ID not found or invalid. |
| DELETE    | Delete         | 405 (Method Not Allowed), unless you want to delete the whole collection—not often desirable.        | 200 (OK). 404 (Not Found), if ID not found or invalid.                     |

### GET
The HTTP GET method is used to \*\*read\*\* (or retrieve) a representation of a resource. In the “happy” (or non-error) path, GET returns a representation in XML or JSON and an HTTP response code of 200 (OK). In an error case, it most often returns a 404 (NOT FOUND) or 400 (BAD REQUEST).

According to the design of the HTTP specification, GET (along with HEAD) requests are used only to read data and not change it. Therefore, when used this way, they are considered safe. That is, they can be called without risk of data modification or corruption—calling it once has the same effect as calling it 10 times, or none at all. Additionally, GET (and HEAD) is idempotent, which means that making multiple identical requests ends up having the same result as a single request.

Do not expose unsafe operations via GET—it should never modify any resources on the server.

**Examples:**

* `GET http://www.example.com/customers/12345`
* `GET http://www.example.com/customers/12345/orders`
* `GET http://www.example.com/buckets/sample`

### POST
The POST verb is most-often utilized to \*\*create\*\* new resources. In particular, it's used to create subordinate resources. That is, subordinate to some other (e.g. parent) resource. In other words, when creating a new resource, POST to the parent and the service takes care of associating the new resource with the parent, assigning an ID (new resource URI), etc.

On successful creation, return HTTP status 201, returning a Location header with a link to the newly-created resource with the 201 HTTP status.

POST is neither safe nor idempotent. It is therefore recommended for non-idempotent resource requests. Making two identical POST requests will most-likely result in two resources containing the same information.

**Examples:**

* `POST http://www.example.com/customers`
* `POST http://www.example.com/customers/12345/orders`

### DELETE

DELETE is pretty easy to understand. It is used to \*\*delete\*\* a resource identified by a URI.

On successful deletion, return HTTP status 200 (OK) along with a response body, perhaps the representation of the deleted item (often demands too much bandwidth), or a wrapped response (see Return Values below). Either that or return HTTP status 204 (NO CONTENT) with no response body. In other words, a 204 status with no body, or the JSEND-style response and HTTP status 200 are the recommended responses.

HTTP-spec-wise, DELETE operations are idempotent. If you DELETE a resource, it's removed. Repeatedly calling DELETE on that resource ends up the same: the resource is gone. If calling DELETE say, decrements a counter (within the resource), the DELETE call is no longer idempotent. As mentioned previously, usage statistics and measurements may be updated while still considering the service idempotent as long as no resource data is changed. Using POST for non-idempotent resource requests is recommended.

There is a caveat about DELETE idempotence, however. Calling DELETE on a resource a second time will often return a 404 (NOT FOUND) since it was already removed and therefore is no longer findable. This, by some opinions, makes DELETE operations no longer idempotent, however, the end-state of the resource is the same. Returning a 404 is acceptable and communicates accurately the status of the call.

**Examples:**

* `DELETE http://www.example.com/customers/12345`
* `DELETE http://www.example.com/customers/12345/orders`
* `DELETE http://www.example.com/bucket/sample`
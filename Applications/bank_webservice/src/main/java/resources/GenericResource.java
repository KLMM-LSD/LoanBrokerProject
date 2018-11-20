/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package resources;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import javax.ws.rs.Consumes;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.UriInfo;
import javax.ws.rs.Produces;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

/**
 * REST Web Service
 *
 * @author Lasse
 */
@Path("bank")
public class GenericResource {

    @Context
    private UriInfo context;

    /**
     * Creates a new instance of GenericResource
     */
    public GenericResource() {
    }

    /**
     * Retrieves representation of an instance of resources.GenericResource
     *
     * @return an instance of java.lang.String
     */
    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public Response getGenericResponse() {
        String text = "Use POST and supply ssn, creditScore, loanAmount, loanDuration";
        return Response.ok(text).build();
    }

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    public Response doSomething(String req) {
        JsonObject ret = new JsonObject();
        JsonParser jp = new JsonParser();
        JsonObject tmp = jp.parse(req).getAsJsonObject();

        ret.addProperty("interestRate", Math.random() * 5 + 1);
        ret.addProperty("ssn", tmp.get("ssn").getAsInt());

        return Response.ok(ret.toString()).build();
    }
}

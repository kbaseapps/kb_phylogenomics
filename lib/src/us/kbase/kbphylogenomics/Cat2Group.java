
package us.kbase.kbphylogenomics;

import java.util.HashMap;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: Cat2Group</p>
 * <pre>
 * category to group
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "namespace",
    "cat"
})
public class Cat2Group {

    @JsonProperty("namespace")
    private String namespace;
    @JsonProperty("cat")
    private String cat;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("namespace")
    public String getNamespace() {
        return namespace;
    }

    @JsonProperty("namespace")
    public void setNamespace(String namespace) {
        this.namespace = namespace;
    }

    public Cat2Group withNamespace(String namespace) {
        this.namespace = namespace;
        return this;
    }

    @JsonProperty("cat")
    public String getCat() {
        return cat;
    }

    @JsonProperty("cat")
    public void setCat(String cat) {
        this.cat = cat;
    }

    public Cat2Group withCat(String cat) {
        this.cat = cat;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((("Cat2Group"+" [namespace=")+ namespace)+", cat=")+ cat)+", additionalProperties=")+ additionalProperties)+"]");
    }

}


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
 * <p>Original spec-file type: get_configure_categories_Input</p>
 * <pre>
 * get_configure_categories()
 * **
 * ** configure the domain categorie names and descriptions
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "params"
})
public class GetConfigureCategoriesInput {

    /**
     * <p>Original spec-file type: view_fxn_profile_Input</p>
     * <pre>
     * view_fxn_profile()
     * **
     * ** show a table/heatmap of general categories or custom gene families for a set of Genomes
     * </pre>
     * 
     */
    @JsonProperty("params")
    private ViewFxnProfileInput params;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    /**
     * <p>Original spec-file type: view_fxn_profile_Input</p>
     * <pre>
     * view_fxn_profile()
     * **
     * ** show a table/heatmap of general categories or custom gene families for a set of Genomes
     * </pre>
     * 
     */
    @JsonProperty("params")
    public ViewFxnProfileInput getParams() {
        return params;
    }

    /**
     * <p>Original spec-file type: view_fxn_profile_Input</p>
     * <pre>
     * view_fxn_profile()
     * **
     * ** show a table/heatmap of general categories or custom gene families for a set of Genomes
     * </pre>
     * 
     */
    @JsonProperty("params")
    public void setParams(ViewFxnProfileInput params) {
        this.params = params;
    }

    public GetConfigureCategoriesInput withParams(ViewFxnProfileInput params) {
        this.params = params;
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
        return ((((("GetConfigureCategoriesInput"+" [params=")+ params)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

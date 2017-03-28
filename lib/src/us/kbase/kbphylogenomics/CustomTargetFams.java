
package us.kbase.kbphylogenomics;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: CustomTargetFams</p>
 * <pre>
 * parameter groups
 * </pre>
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "target_fams",
    "extra_target_fam_groups_COG",
    "extra_target_fam_groups_PFAM",
    "extra_target_fam_groups_TIGR",
    "extra_target_fam_groups_SEED"
})
public class CustomTargetFams {

    @JsonProperty("target_fams")
    private List<String> targetFams;
    @JsonProperty("extra_target_fam_groups_COG")
    private List<String> extraTargetFamGroupsCOG;
    @JsonProperty("extra_target_fam_groups_PFAM")
    private List<String> extraTargetFamGroupsPFAM;
    @JsonProperty("extra_target_fam_groups_TIGR")
    private List<String> extraTargetFamGroupsTIGR;
    @JsonProperty("extra_target_fam_groups_SEED")
    private List<String> extraTargetFamGroupsSEED;
    private Map<java.lang.String, Object> additionalProperties = new HashMap<java.lang.String, Object>();

    @JsonProperty("target_fams")
    public List<String> getTargetFams() {
        return targetFams;
    }

    @JsonProperty("target_fams")
    public void setTargetFams(List<String> targetFams) {
        this.targetFams = targetFams;
    }

    public CustomTargetFams withTargetFams(List<String> targetFams) {
        this.targetFams = targetFams;
        return this;
    }

    @JsonProperty("extra_target_fam_groups_COG")
    public List<String> getExtraTargetFamGroupsCOG() {
        return extraTargetFamGroupsCOG;
    }

    @JsonProperty("extra_target_fam_groups_COG")
    public void setExtraTargetFamGroupsCOG(List<String> extraTargetFamGroupsCOG) {
        this.extraTargetFamGroupsCOG = extraTargetFamGroupsCOG;
    }

    public CustomTargetFams withExtraTargetFamGroupsCOG(List<String> extraTargetFamGroupsCOG) {
        this.extraTargetFamGroupsCOG = extraTargetFamGroupsCOG;
        return this;
    }

    @JsonProperty("extra_target_fam_groups_PFAM")
    public List<String> getExtraTargetFamGroupsPFAM() {
        return extraTargetFamGroupsPFAM;
    }

    @JsonProperty("extra_target_fam_groups_PFAM")
    public void setExtraTargetFamGroupsPFAM(List<String> extraTargetFamGroupsPFAM) {
        this.extraTargetFamGroupsPFAM = extraTargetFamGroupsPFAM;
    }

    public CustomTargetFams withExtraTargetFamGroupsPFAM(List<String> extraTargetFamGroupsPFAM) {
        this.extraTargetFamGroupsPFAM = extraTargetFamGroupsPFAM;
        return this;
    }

    @JsonProperty("extra_target_fam_groups_TIGR")
    public List<String> getExtraTargetFamGroupsTIGR() {
        return extraTargetFamGroupsTIGR;
    }

    @JsonProperty("extra_target_fam_groups_TIGR")
    public void setExtraTargetFamGroupsTIGR(List<String> extraTargetFamGroupsTIGR) {
        this.extraTargetFamGroupsTIGR = extraTargetFamGroupsTIGR;
    }

    public CustomTargetFams withExtraTargetFamGroupsTIGR(List<String> extraTargetFamGroupsTIGR) {
        this.extraTargetFamGroupsTIGR = extraTargetFamGroupsTIGR;
        return this;
    }

    @JsonProperty("extra_target_fam_groups_SEED")
    public List<String> getExtraTargetFamGroupsSEED() {
        return extraTargetFamGroupsSEED;
    }

    @JsonProperty("extra_target_fam_groups_SEED")
    public void setExtraTargetFamGroupsSEED(List<String> extraTargetFamGroupsSEED) {
        this.extraTargetFamGroupsSEED = extraTargetFamGroupsSEED;
    }

    public CustomTargetFams withExtraTargetFamGroupsSEED(List<String> extraTargetFamGroupsSEED) {
        this.extraTargetFamGroupsSEED = extraTargetFamGroupsSEED;
        return this;
    }

    @JsonAnyGetter
    public Map<java.lang.String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(java.lang.String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public java.lang.String toString() {
        return ((((((((((((("CustomTargetFams"+" [targetFams=")+ targetFams)+", extraTargetFamGroupsCOG=")+ extraTargetFamGroupsCOG)+", extraTargetFamGroupsPFAM=")+ extraTargetFamGroupsPFAM)+", extraTargetFamGroupsTIGR=")+ extraTargetFamGroupsTIGR)+", extraTargetFamGroupsSEED=")+ extraTargetFamGroupsSEED)+", additionalProperties=")+ additionalProperties)+"]");
    }

}

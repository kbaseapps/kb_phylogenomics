package us.kbase.kbphylogenomics;

import com.fasterxml.jackson.core.type.TypeReference;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import us.kbase.auth.AuthToken;
import us.kbase.common.service.JsonClientCaller;
import us.kbase.common.service.JsonClientException;
import us.kbase.common.service.RpcContext;
import us.kbase.common.service.UnauthorizedException;

/**
 * <p>Original spec-file module name: kb_phylogenomics</p>
 * <pre>
 * A KBase module: kb_phylogenomics
 * This module contains methods for running and visualizing results of phylogenomics and comparative genomics analyses
 * </pre>
 */
public class KbPhylogenomicsClient {
    private JsonClientCaller caller;
    private String serviceVersion = null;


    /** Constructs a client with a custom URL and no user credentials.
     * @param url the URL of the service.
     */
    public KbPhylogenomicsClient(URL url) {
        caller = new JsonClientCaller(url);
    }
    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param token the user's authorization token.
     * @throws UnauthorizedException if the token is not valid.
     * @throws IOException if an IOException occurs when checking the token's
     * validity.
     */
    public KbPhylogenomicsClient(URL url, AuthToken token) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, token);
    }

    /** Constructs a client with a custom URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public KbPhylogenomicsClient(URL url, String user, String password) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password);
    }

    /** Constructs a client with a custom URL
     * and a custom authorization service URL.
     * @param url the URL of the service.
     * @param user the user name.
     * @param password the password for the user name.
     * @param auth the URL of the authorization server.
     * @throws UnauthorizedException if the credentials are not valid.
     * @throws IOException if an IOException occurs when checking the user's
     * credentials.
     */
    public KbPhylogenomicsClient(URL url, String user, String password, URL auth) throws UnauthorizedException, IOException {
        caller = new JsonClientCaller(url, user, password, auth);
    }

    /** Get the token this client uses to communicate with the server.
     * @return the authorization token.
     */
    public AuthToken getToken() {
        return caller.getToken();
    }

    /** Get the URL of the service with which this client communicates.
     * @return the service URL.
     */
    public URL getURL() {
        return caller.getURL();
    }

    /** Set the timeout between establishing a connection to a server and
     * receiving a response. A value of zero or null implies no timeout.
     * @param milliseconds the milliseconds to wait before timing out when
     * attempting to read from a server.
     */
    public void setConnectionReadTimeOut(Integer milliseconds) {
        this.caller.setConnectionReadTimeOut(milliseconds);
    }

    /** Check if this client allows insecure http (vs https) connections.
     * @return true if insecure connections are allowed.
     */
    public boolean isInsecureHttpConnectionAllowed() {
        return caller.isInsecureHttpConnectionAllowed();
    }

    /** Deprecated. Use isInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public boolean isAuthAllowedForHttp() {
        return caller.isAuthAllowedForHttp();
    }

    /** Set whether insecure http (vs https) connections should be allowed by
     * this client.
     * @param allowed true to allow insecure connections. Default false
     */
    public void setIsInsecureHttpConnectionAllowed(boolean allowed) {
        caller.setInsecureHttpConnectionAllowed(allowed);
    }

    /** Deprecated. Use setIsInsecureHttpConnectionAllowed().
     * @deprecated
     */
    public void setAuthAllowedForHttp(boolean isAuthAllowedForHttp) {
        caller.setAuthAllowedForHttp(isAuthAllowedForHttp);
    }

    /** Set whether all SSL certificates, including self-signed certificates,
     * should be trusted.
     * @param trustAll true to trust all certificates. Default false.
     */
    public void setAllSSLCertificatesTrusted(final boolean trustAll) {
        caller.setAllSSLCertificatesTrusted(trustAll);
    }
    
    /** Check if this client trusts all SSL certificates, including
     * self-signed certificates.
     * @return true if all certificates are trusted.
     */
    public boolean isAllSSLCertificatesTrusted() {
        return caller.isAllSSLCertificatesTrusted();
    }
    /** Sets streaming mode on. In this case, the data will be streamed to
     * the server in chunks as it is read from disk rather than buffered in
     * memory. Many servers are not compatible with this feature.
     * @param streamRequest true to set streaming mode on, false otherwise.
     */
    public void setStreamingModeOn(boolean streamRequest) {
        caller.setStreamingModeOn(streamRequest);
    }

    /** Returns true if streaming mode is on.
     * @return true if streaming mode is on.
     */
    public boolean isStreamingModeOn() {
        return caller.isStreamingModeOn();
    }

    public void _setFileForNextRpcResponse(File f) {
        caller.setFileForNextRpcResponse(f);
    }

    public String getServiceVersion() {
        return this.serviceVersion;
    }

    public void setServiceVersion(String newValue) {
        this.serviceVersion = newValue;
    }

    /**
     * <p>Original spec-file function name: build_gene_tree</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.BuildGeneTreeInput BuildGeneTreeInput} (original type "build_gene_tree_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.BuildGeneTreeOutput BuildGeneTreeOutput} (original type "build_gene_tree_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public BuildGeneTreeOutput buildGeneTree(BuildGeneTreeInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<BuildGeneTreeOutput>> retType = new TypeReference<List<BuildGeneTreeOutput>>() {};
        List<BuildGeneTreeOutput> res = caller.jsonrpcCall("kb_phylogenomics.build_gene_tree", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: build_strain_tree</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.BuildStrainTreeInput BuildStrainTreeInput} (original type "build_strain_tree_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.BuildStrainTreeOutput BuildStrainTreeOutput} (original type "build_strain_tree_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public BuildStrainTreeOutput buildStrainTree(BuildStrainTreeInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<BuildStrainTreeOutput>> retType = new TypeReference<List<BuildStrainTreeOutput>>() {};
        List<BuildStrainTreeOutput> res = caller.jsonrpcCall("kb_phylogenomics.build_strain_tree", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: build_pangenome_species_tree</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.BuildPangenomeSpeciesTreeInput BuildPangenomeSpeciesTreeInput} (original type "build_pangenome_species_tree_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.BuildPangenomeSpeciesTreeOutput BuildPangenomeSpeciesTreeOutput} (original type "build_pangenome_species_tree_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public BuildPangenomeSpeciesTreeOutput buildPangenomeSpeciesTree(BuildPangenomeSpeciesTreeInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<BuildPangenomeSpeciesTreeOutput>> retType = new TypeReference<List<BuildPangenomeSpeciesTreeOutput>>() {};
        List<BuildPangenomeSpeciesTreeOutput> res = caller.jsonrpcCall("kb_phylogenomics.build_pangenome_species_tree", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: view_tree</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.ViewTreeInput ViewTreeInput} (original type "view_tree_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.ViewTreeOutput ViewTreeOutput} (original type "view_tree_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ViewTreeOutput viewTree(ViewTreeInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ViewTreeOutput>> retType = new TypeReference<List<ViewTreeOutput>>() {};
        List<ViewTreeOutput> res = caller.jsonrpcCall("kb_phylogenomics.view_tree", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: trim_speciestree_to_genomeset</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.TrimSpeciestreeToGenomesetInput TrimSpeciestreeToGenomesetInput} (original type "trim_speciestree_to_genomeset_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.TrimSpeciestreeToGenomesetOutput TrimSpeciestreeToGenomesetOutput} (original type "trim_speciestree_to_genomeset_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public TrimSpeciestreeToGenomesetOutput trimSpeciestreeToGenomeset(TrimSpeciestreeToGenomesetInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<TrimSpeciestreeToGenomesetOutput>> retType = new TypeReference<List<TrimSpeciestreeToGenomesetOutput>>() {};
        List<TrimSpeciestreeToGenomesetOutput> res = caller.jsonrpcCall("kb_phylogenomics.trim_speciestree_to_genomeset", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: trim_genetree_to_genomeset</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.TrimGenetreeToGenomesetInput TrimGenetreeToGenomesetInput} (original type "trim_genetree_to_genomeset_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.TrimGenetreeToGenomesetOutput TrimGenetreeToGenomesetOutput} (original type "trim_genetree_to_genomeset_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public TrimGenetreeToGenomesetOutput trimGenetreeToGenomeset(TrimGenetreeToGenomesetInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<TrimGenetreeToGenomesetOutput>> retType = new TypeReference<List<TrimGenetreeToGenomesetOutput>>() {};
        List<TrimGenetreeToGenomesetOutput> res = caller.jsonrpcCall("kb_phylogenomics.trim_genetree_to_genomeset", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: build_microbial_speciestree</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.BuildMicrobialSpeciestreeInput BuildMicrobialSpeciestreeInput} (original type "build_microbial_speciestree_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.BuildMicrobialSpeciestreeOutput BuildMicrobialSpeciestreeOutput} (original type "build_microbial_speciestree_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public BuildMicrobialSpeciestreeOutput buildMicrobialSpeciestree(BuildMicrobialSpeciestreeInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<BuildMicrobialSpeciestreeOutput>> retType = new TypeReference<List<BuildMicrobialSpeciestreeOutput>>() {};
        List<BuildMicrobialSpeciestreeOutput> res = caller.jsonrpcCall("kb_phylogenomics.build_microbial_speciestree", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: localize_DomainAnnotations</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.LocalizeDomainAnnotationsInput LocalizeDomainAnnotationsInput} (original type "localize_DomainAnnotations_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.LocalizeDomainAnnotationsOutput LocalizeDomainAnnotationsOutput} (original type "localize_DomainAnnotations_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public LocalizeDomainAnnotationsOutput localizeDomainAnnotations(LocalizeDomainAnnotationsInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<LocalizeDomainAnnotationsOutput>> retType = new TypeReference<List<LocalizeDomainAnnotationsOutput>>() {};
        List<LocalizeDomainAnnotationsOutput> res = caller.jsonrpcCall("kb_phylogenomics.localize_DomainAnnotations", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: run_DomainAnnotation_Sets</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.RunDomainAnnotationSetsInput RunDomainAnnotationSetsInput} (original type "run_DomainAnnotation_Sets_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.RunDomainAnnotationSetsOutput RunDomainAnnotationSetsOutput} (original type "run_DomainAnnotation_Sets_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public RunDomainAnnotationSetsOutput runDomainAnnotationSets(RunDomainAnnotationSetsInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<RunDomainAnnotationSetsOutput>> retType = new TypeReference<List<RunDomainAnnotationSetsOutput>>() {};
        List<RunDomainAnnotationSetsOutput> res = caller.jsonrpcCall("kb_phylogenomics.run_DomainAnnotation_Sets", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: view_fxn_profile</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.ViewFxnProfileInput ViewFxnProfileInput} (original type "view_fxn_profile_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.ViewFxnProfileOutput ViewFxnProfileOutput} (original type "view_fxn_profile_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ViewFxnProfileOutput viewFxnProfile(ViewFxnProfileInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ViewFxnProfileOutput>> retType = new TypeReference<List<ViewFxnProfileOutput>>() {};
        List<ViewFxnProfileOutput> res = caller.jsonrpcCall("kb_phylogenomics.view_fxn_profile", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: view_fxn_profile_featureSet</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.ViewFxnProfileFeatureSetInput ViewFxnProfileFeatureSetInput} (original type "view_fxn_profile_featureSet_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.ViewFxnProfileFeatureSetOutput ViewFxnProfileFeatureSetOutput} (original type "view_fxn_profile_featureSet_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ViewFxnProfileFeatureSetOutput viewFxnProfileFeatureSet(ViewFxnProfileFeatureSetInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ViewFxnProfileFeatureSetOutput>> retType = new TypeReference<List<ViewFxnProfileFeatureSetOutput>>() {};
        List<ViewFxnProfileFeatureSetOutput> res = caller.jsonrpcCall("kb_phylogenomics.view_fxn_profile_featureSet", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: view_fxn_profile_phylo</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.ViewFxnProfilePhyloInput ViewFxnProfilePhyloInput} (original type "view_fxn_profile_phylo_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.ViewFxnProfilePhyloOutput ViewFxnProfilePhyloOutput} (original type "view_fxn_profile_phylo_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ViewFxnProfilePhyloOutput viewFxnProfilePhylo(ViewFxnProfilePhyloInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ViewFxnProfilePhyloOutput>> retType = new TypeReference<List<ViewFxnProfilePhyloOutput>>() {};
        List<ViewFxnProfilePhyloOutput> res = caller.jsonrpcCall("kb_phylogenomics.view_fxn_profile_phylo", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: view_genome_circle_plot</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.ViewGenomeCirclePlotInput ViewGenomeCirclePlotInput} (original type "view_genome_circle_plot_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.ViewGenomeCirclePlotOutput ViewGenomeCirclePlotOutput} (original type "view_genome_circle_plot_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ViewGenomeCirclePlotOutput viewGenomeCirclePlot(ViewGenomeCirclePlotInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ViewGenomeCirclePlotOutput>> retType = new TypeReference<List<ViewGenomeCirclePlotOutput>>() {};
        List<ViewGenomeCirclePlotOutput> res = caller.jsonrpcCall("kb_phylogenomics.view_genome_circle_plot", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: view_pan_circle_plot</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.ViewPanCirclePlotInput ViewPanCirclePlotInput} (original type "view_pan_circle_plot_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.ViewPanCirclePlotOutput ViewPanCirclePlotOutput} (original type "view_pan_circle_plot_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ViewPanCirclePlotOutput viewPanCirclePlot(ViewPanCirclePlotInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ViewPanCirclePlotOutput>> retType = new TypeReference<List<ViewPanCirclePlotOutput>>() {};
        List<ViewPanCirclePlotOutput> res = caller.jsonrpcCall("kb_phylogenomics.view_pan_circle_plot", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: view_pan_accumulation_plot</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.ViewPanAccumulationPlotInput ViewPanAccumulationPlotInput} (original type "view_pan_accumulation_plot_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.ViewPanAccumulationPlotOutput ViewPanAccumulationPlotOutput} (original type "view_pan_accumulation_plot_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ViewPanAccumulationPlotOutput viewPanAccumulationPlot(ViewPanAccumulationPlotInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ViewPanAccumulationPlotOutput>> retType = new TypeReference<List<ViewPanAccumulationPlotOutput>>() {};
        List<ViewPanAccumulationPlotOutput> res = caller.jsonrpcCall("kb_phylogenomics.view_pan_accumulation_plot", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: view_pan_flower_venn</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.ViewPanFlowerVennInput ViewPanFlowerVennInput} (original type "view_pan_flower_venn_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.ViewPanFlowerVennOutput ViewPanFlowerVennOutput} (original type "view_pan_flower_venn_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ViewPanFlowerVennOutput viewPanFlowerVenn(ViewPanFlowerVennInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ViewPanFlowerVennOutput>> retType = new TypeReference<List<ViewPanFlowerVennOutput>>() {};
        List<ViewPanFlowerVennOutput> res = caller.jsonrpcCall("kb_phylogenomics.view_pan_flower_venn", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: view_pan_pairwise_overlap</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.ViewPanPairwiseOverlapInput ViewPanPairwiseOverlapInput} (original type "view_pan_pairwise_overlap_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.ViewPanPairwiseOverlapOutput ViewPanPairwiseOverlapOutput} (original type "view_pan_pairwise_overlap_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ViewPanPairwiseOverlapOutput viewPanPairwiseOverlap(ViewPanPairwiseOverlapInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ViewPanPairwiseOverlapOutput>> retType = new TypeReference<List<ViewPanPairwiseOverlapOutput>>() {};
        List<ViewPanPairwiseOverlapOutput> res = caller.jsonrpcCall("kb_phylogenomics.view_pan_pairwise_overlap", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: view_pan_phylo</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.ViewPanPhyloInput ViewPanPhyloInput} (original type "view_pan_phylo_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.ViewPanPhyloOutput ViewPanPhyloOutput} (original type "view_pan_phylo_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public ViewPanPhyloOutput viewPanPhylo(ViewPanPhyloInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<ViewPanPhyloOutput>> retType = new TypeReference<List<ViewPanPhyloOutput>>() {};
        List<ViewPanPhyloOutput> res = caller.jsonrpcCall("kb_phylogenomics.view_pan_phylo", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: find_homologs_with_genome_context</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.FindHomologsWithGenomeContextInput FindHomologsWithGenomeContextInput} (original type "find_homologs_with_genome_context_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.FindHomologsWithGenomeContextOutput FindHomologsWithGenomeContextOutput} (original type "find_homologs_with_genome_context_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public FindHomologsWithGenomeContextOutput findHomologsWithGenomeContext(FindHomologsWithGenomeContextInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<FindHomologsWithGenomeContextOutput>> retType = new TypeReference<List<FindHomologsWithGenomeContextOutput>>() {};
        List<FindHomologsWithGenomeContextOutput> res = caller.jsonrpcCall("kb_phylogenomics.find_homologs_with_genome_context", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    /**
     * <p>Original spec-file function name: get_configure_categories</p>
     * <pre>
     * </pre>
     * @param   params   instance of type {@link us.kbase.kbphylogenomics.GetConfigureCategoriesInput GetConfigureCategoriesInput} (original type "get_configure_categories_Input")
     * @return   parameter "output" of type {@link us.kbase.kbphylogenomics.GetConfigureCategoriesOutput GetConfigureCategoriesOutput} (original type "get_configure_categories_Output")
     * @throws IOException if an IO exception occurs
     * @throws JsonClientException if a JSON RPC exception occurs
     */
    public GetConfigureCategoriesOutput getConfigureCategories(GetConfigureCategoriesInput params, RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        args.add(params);
        TypeReference<List<GetConfigureCategoriesOutput>> retType = new TypeReference<List<GetConfigureCategoriesOutput>>() {};
        List<GetConfigureCategoriesOutput> res = caller.jsonrpcCall("kb_phylogenomics.get_configure_categories", args, retType, true, true, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }

    public Map<String, Object> status(RpcContext... jsonRpcContext) throws IOException, JsonClientException {
        List<Object> args = new ArrayList<Object>();
        TypeReference<List<Map<String, Object>>> retType = new TypeReference<List<Map<String, Object>>>() {};
        List<Map<String, Object>> res = caller.jsonrpcCall("kb_phylogenomics.status", args, retType, true, false, jsonRpcContext, this.serviceVersion);
        return res.get(0);
    }
}
